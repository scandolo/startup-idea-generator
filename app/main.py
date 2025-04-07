from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="PitchSlap API", description="Generate unique startup ideas based on requirements")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PitchRequest(BaseModel):
    skills: str
    interests: str
    experience: str
    preferences: Optional[str] = None
    constraints: Optional[str] = None
    idea_count: Optional[int] = 3

class PitchResponse(BaseModel):
    ideas: List[str]

@app.get("/")
async def root():
    return {"message": "Welcome to PitchSlap API! Use /generate endpoint to create startup ideas."}

@app.post("/generate", response_model=PitchResponse)
async def generate_ideas(request: PitchRequest):
    try:
        # Construct the prompt
        prompt = f"""Based on the user's background, generate {request.idea_count} unique and innovative startup ideas:
        
Skills: {request.skills}
Interests: {request.interests}
Experience: {request.experience}
"""
        
        if request.preferences:
            prompt += f"Preferences: {request.preferences}\n"
                
        if request.constraints:
            prompt += f"Constraints: {request.constraints}\n"
                
        prompt += "\nFor each idea, provide a concise name and 2-3 sentence description including the target market and problem being solved. Make these ideas creative, feasible, and market-ready, leveraging the user's unique skills and experience."

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a career and startup advisor who specializes in matching people's skills and interests with innovative business opportunities. You analyze a person's background and suggest tailored startup ideas that leverage their unique strengths."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=1500
        )
        
        # Extract and format ideas
        raw_ideas = response.choices[0].message.content.strip().split("\n\n")
        formatted_ideas = [idea.strip() for idea in raw_ideas if idea.strip()]
        
        return PitchResponse(ideas=formatted_ideas)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating ideas: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 