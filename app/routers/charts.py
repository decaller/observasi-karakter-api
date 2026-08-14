import io
import json
import re
import random
from fastapi import APIRouter, Query, HTTPException, Response
import matplotlib.pyplot as plt
import cairosvg

router = APIRouter(prefix="/api/v1/chart", tags=["Charts"])

@router.get("/obskarakter", responses={200: {"content": {"image/png": {}}}})
async def chart_obskarakter(scores: str = Query(..., description="JSON array of scores. Example: [{'kategori': 'Aqidah', 'score': 80}]")):
    try:
        parsed_scores = json.loads(scores)
        if not isinstance(parsed_scores, list):
            raise ValueError("Scores must be a JSON array")
        
        categories = [item['kategori'][:15] + ".." if len(item['kategori']) > 15 else item['kategori'] for item in parsed_scores]
        real_scores = [item.get('score', 0) for item in parsed_scores]
        
        # Mock Expected Scores (e.g. standard expectation based on age)
        expected_scores = [100 for _ in parsed_scores]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot Expected
        bars_exp = ax.bar(categories, expected_scores, color='#e0e0e0', label='Ekspektasi')
        # Plot Real
        bars_real = ax.bar(categories, real_scores, color='#4CAF50', label='Realita', alpha=0.9)
        
        ax.set_ylabel('Skor')
        ax.set_title('Realita vs Ekspektasi (Karakter)')
        ax.set_ylim(0, 110)
        ax.legend()
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Save to bytes
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close(fig)
        
        return Response(content=buf.getvalue(), media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.get("/obsbakat", responses={200: {"content": {"image/png": {}}}})
async def chart_obsbakat():
    """Renders the SVG from tb40 to PNG with mocked dynamic colors for demonstration."""
    try:
        svg_path = "api-tb40-explore/api/v0.1/tb40/tb40.svg"
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
            
        # We need to replace Handlebars like {{tb40.result.[18].[0].color}}
        # We will map them to some realistic colors
        # Red (Top), Yellow (High), Grey (Mid), Black (Low)
        palette = ['#e74c3c', '#f1c40f', '#95a5a6', '#2c3e50', '#3498db']
        
        def replacer(match):
            # Pick a random or pseudo-random color for mockup purposes
            # A real implementation would parse the scores param and map it properly.
            return random.choice(palette)
            
        # Regex to match {{tb40.result.[X].[Y].color}}
        pattern = r"\{\{tb40\.result\.\[\d+\]\.\[\d+\]\.color\}\}"
        colored_svg = re.sub(pattern, replacer, svg_content)
        
        # Convert SVG string to PNG bytes using cairosvg
        png_bytes = cairosvg.svg2png(bytestring=colored_svg.encode('utf-8'))
        
        return Response(content=png_bytes, media_type="image/png")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SVG generation failed: {str(e)}")
