import os
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from database import create_document

app = FastAPI(title="AC Maintenance Service API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "AC Maintenance Service Backend Running"}

@app.get("/api/pain-points")
def get_pain_points():
    """Return researched pain points for AC owners/operators."""
    pain_points = [
        "Frequent breakdowns during peak heat",
        "Inconsistent cooling and hot/cold spots",
        "High electricity bills",
        "Poor air quality, dust and allergens",
        "Water leaks or drain line clogs",
        "Unpleasant odors when the unit starts",
        "Noisy operation or vibrations",
        "Short equipment lifespan due to poor maintenance",
        "Unexpected repair costs and downtime",
        "Thermostat inaccuracies and comfort issues",
        "Slow response from service providers",
        "Lack of maintenance records for compliance/warranty",
    ]
    return {"pain_points": pain_points}

@app.get("/api/maintenance-tasks")
def maintenance_tasks() -> Dict[str, Any]:
    """Evidence-based routine maintenance tasks for split and ducted AC systems (1–50 ton)."""
    tasks = [
        {"category": "Airflow & Filtration", "items": [
            "Inspect and clean/replace air filters (MERV rating as specified)",
            "Measure external static pressure and adjust airflow to manufacturer specs",
            "Inspect supply/return grilles and ductwork for blockages or leaks",
        ]},
        {"category": "Evaporator & Condenser Coils", "items": [
            "Visual inspection of evaporator and condenser coils",
            "Clean coils with appropriate method (dry brush, fin combs, or coil cleaner)",
            "Straighten bent fins to restore heat transfer",
        ]},
        {"category": "Condensate Management", "items": [
            "Flush and clear condensate drain line and trap",
            "Test condensate pump operation (if installed)",
            "Check drain pan for rust, algae, or overflow sensors",
        ]},
        {"category": "Refrigerant Circuit", "items": [
            "Check for oil stains and obvious leaks",
            "Verify superheat/subcooling and compare to design conditions",
            "Tighten service caps and inspect Schrader cores",
        ]},
        {"category": "Electrical & Controls", "items": [
            "Inspect contactors, relays, capacitors, and wiring for wear/overheating",
            "Torque terminal connections to spec",
            "Test safety controls and float switches",
            "Calibrate thermostat and verify setpoints/schedules",
        ]},
        {"category": "Mechanical Components", "items": [
            "Inspect blower wheel, motor bearings, and belts/pulleys; adjust tension",
            "Check fan blades and motor mounts for balance and vibration",
            "Lubricate bearings where applicable",
        ]},
        {"category": "Performance Verification", "items": [
            "Measure supply/return air temperatures; calculate temperature split",
            "Record amperage/voltage vs nameplate",
            "Verify overall system capacity aligns with 1–50 ton application",
        ]},
        {"category": "Documentation", "items": [
            "Record measurements and maintenance actions",
            "Note deficiencies and recommended corrective actions",
            "Maintain logs to support warranty and compliance",
        ]},
    ]

    intervals = [
        {"interval": "Monthly / Bi-Monthly", "recommended": [
            "Filter inspection and replacement",
            "Visual check of condensate drains",
            "Basic visual inspection of outdoor unit",
        ]},
        {"interval": "Quarterly", "recommended": [
            "Coil inspection/cleaning as needed",
            "Drain line flushing",
            "Electrical inspection and torque check",
        ]},
        {"interval": "Bi-Annual", "recommended": [
            "Refrigerant performance check (superheat/subcool)",
            "Thermostat calibration and control verification",
            "Static pressure and airflow balancing",
        ]},
        {"interval": "Annual", "recommended": [
            "Full system tune-up and performance benchmarking",
            "Ductwork inspection for leaks and insulation",
            "Comprehensive documentation and lifecycle advisory",
        ]},
    ]

    system_types = [
        "Split (ducted/non-ducted)",
        "Ducted package units",
        "VRF/VRV (upon request)",
    ]

    return {
        "scope": "Preventive maintenance for residential, commercial, and light-industrial AC systems",
        "capacity_range": "1 to 50 ton (12,000 to 600,000 Btu/h)",
        "system_types": system_types,
        "tasks": tasks,
        "interval_guidance": intervals,
    }

class LeadRequest(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    unit_types: Optional[List[str]] = None
    units_count: Optional[int] = None
    capacity_tonnage: Optional[str] = None
    preferred_interval: Optional[str] = None
    pain_points: Optional[List[str]] = None
    message: Optional[str] = None

@app.post("/api/leads")
def create_lead(lead: LeadRequest):
    try:
        lead_id = create_document("lead", lead.model_dump())
        return {"status": "success", "id": lead_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        from database import db
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    import os as _os
    response["database_url"] = "✅ Set" if _os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if _os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
