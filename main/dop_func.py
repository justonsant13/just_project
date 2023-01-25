def getting_salary(vac, salary):
    salary += f"{vac['salary']['from']}"
    if vac.get("salary", {}).get("to", ""):
        salary += f" -- {vac['salary']['to']}"
    salary += f" {vac['salary']['currency']}"
    return salary