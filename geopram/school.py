"""School domain constants and record validation."""
SCHOOL_COLLECTIONS=("students","staff","courses","classes","attendance","fees","enrollments","timetables","exams","grades","parents")
def validate_student(record):
    if not record.get("full_name") and not record.get("name"): raise ValueError("Student name is required")
    return {**record,"status":record.get("status","active")}
