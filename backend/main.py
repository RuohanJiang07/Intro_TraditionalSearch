from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from vector_search import schematic_search
import sqlite3
import numpy as np
import os

app = FastAPI(title="Search API (Vector + Traditional)")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class SearchQuery(BaseModel):
    query: str

class SearchResult(BaseModel):
    Name: str
    Category: str
    Label: str
    Profile_Chunk: str
    Similarity: Optional[float] = None 


# VECTOR SEARCH ENDPOINT
@app.post("/api/search")
async def vector_search(query: SearchQuery) -> List[dict]:
    try:
        results = schematic_search(query.query)
        if results.empty:
            return []
        
        results_list = results.to_dict('records')
        
        for result in results_list:
            result['Similarity'] = float(min(max(result.get('Similarity', 0.0), 0.0), 1.0))
            for key, value in result.items():
                if isinstance(value, float) and (np.isnan(value) or np.isinf(value)):
                    result[key] = 0.0
        
        return results_list
    except Exception as e:
        print(f"Vector Search error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# TRADITIONAL SEARCH ENDPOINT
@app.post("/api/traditional_search")
async def traditional_search(query: SearchQuery) -> List[dict]:
    DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/experts.db'))
    print("Database Path:", DB_PATH)
    print("Search Query:", query.query)

    if not query.query.strip():
        raise HTTPException(status_code=400, detail="Query parameter is required")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # SQL Search Query
        search_query = """
        SELECT name AS Name, category AS Category, label AS Label, profile AS Profile_Chunk, url AS URL
        FROM expert_profiles
        WHERE name LIKE ?
        OR label LIKE ?
        OR profile LIKE ?
        """
        cursor.execute(search_query, (f'%{query.query}%', f'%{query.query}%', f'%{query.query}%'))
        
        rows = cursor.fetchall()
        print("Number of Results:", len(rows))
        
        conn.close()

        results = []
        for row in rows:
            profile_text = row["Profile_Chunk"] or ""
            truncated_profile = (profile_text[:200] + '...') if len(profile_text) > 200 else profile_text  # Limit to 200 characters
            
            results.append({
                "Name": row["Name"],
                "Category": row["Category"],
                "Label": row["Label"],
                "Profile_Chunk": truncated_profile,
                "URL": row["URL"]
            })
        
        print("Results:", results)
        return results
    
    except Exception as e:
        print(f"Traditional Search error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
