import json
from datetime import datetime

def logChanges(changelog, prev, new):
    changes = []
    for field in prev:
      if prev[field] != new[field]:
        changes.append({"field": field, "from": prev[field], "to": new[field]})
    changelog.append({"from": prev, "to": new, "changes": changes})
  
def deduplicate(leads):
  changelog = []
  deduplicated = {}
  for idx, lead in enumerate(leads):
    id = lead["_id"]
    email = lead["email"]
    date = datetime.fromisoformat(lead["entryDate"])
    if id in deduplicated:
      existingLead = deduplicated[id]
      existingEmail, existingDate = existingLead["email"], datetime.fromisoformat(existingLead["entryDate"])
      if existingDate < date or (existingDate == date and leads.index(existingLead) < idx):
        logChanges(changelog, existingLead, lead)
        if existingEmail != email: del deduplicated[existingEmail]
        deduplicated[id] = lead
        deduplicated[email] = lead
    elif email in deduplicated:
      existingLead = deduplicated[email]
      existingId, existingDate = existingLead["_id"], datetime.fromisoformat(existingLead["entryDate"])
      if existingDate < date or (existingDate == date and leads.index(existingLead) < idx):
        logChanges(changelog, existingLead, lead)
        if existingId != id: del deduplicated[existingId]
        deduplicated[email] = lead
        deduplicated[id] = lead
    else:
      deduplicated[id] = lead
      deduplicated[email] = lead

  deduplicated = list({lead["_id"]: lead for lead in deduplicated.values()}.values())  # since there are both lead["email"] and lead["_id"]convert to list to retain original format,
  return deduplicated, changelog

def main():
  try:
    jsonFile = input("Enter the JSON file path: ")
    with open(jsonFile, 'r') as file:
      data = json.load(file)
      deduplicatedLeads, changelog = deduplicate(data["leads"])
      newData = {"leads": deduplicatedLeads}

      outputFile = "deduplicated_leads.json"
      with open(outputFile, 'w') as file:
        json.dump(newData, file, indent=2)
      print(f"Deduplicated leads written to {outputFile}")
      
      changelogFile = "changelog.json"
      with open(changelogFile, 'w') as file:
        json.dump(changelog, file, indent=2)
      print(f"Changelog written to {changelogFile}")

        
  except Exception as e:
    print(e)

if __name__ == '__main__':
  main()