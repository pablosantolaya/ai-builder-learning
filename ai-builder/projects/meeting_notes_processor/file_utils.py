import json
import os

def read_file(filepath):
    try:
        with open(filepath, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None

def save_json_results(results,output_dir, timestamp):
    try:
        filepath = os.path.join(output_dir, f"meeting_results_{timestamp}.json")
        directory = os.path.dirname(filepath)
        if directory:
            os.makedirs(directory, exist_ok=True)        
        with open(filepath, "w") as f:
            json.dump(results, f, indent=4)
    
    except Exception as e:
        print(f"Error saving results: {e}")

def save_text_report(results, output_dir, timestamp):
    
    report = f"MEETING SUMMARY\n"
    if results.get("meeting_date"):
        report += f"Date: {results['meeting_date']}\n"
    else:
        report += f"Date: Unspecified\n"
    report += f"Attendees: "
    report += f"{', '.join(results['attendees'])}\n"
    report += f"\n\nSummary:\n"
    report += f"{results['summary']}\n\n"
    report += f"Decisions:\n"
    for decision in results["decisions"]:
        report += f"   - {decision}\n"
    report += f"\n\nAction Items:\n"
    for action_item in results["action_items"]:
        if action_item.get("deadline"):
            report += f"   - {action_item['owner']}: {action_item['task']} ({action_item['deadline']})\n"
        else:
            report += f"   - {action_item['owner']}: {action_item['task']}\n"   
    report += f"\n\nOpen Questions:\n"
    for question in results["open_questions"]:
        report += f"   - {question}\n"   

    try:
        filepath = os.path.join(output_dir, f"meeting_summary_{timestamp}.txt")
        directory = os.path.dirname(filepath)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(filepath, "w") as f:
            f.write(report)
    
    except Exception as e:
        print(f"Error saving report: {e}")

def generate_follow_up_email(results, output_dir, timestamp):

    if results.get("meeting_date"):
        meeting_date = "on " + results["meeting_date"]
    else:
        meeting_date = "today"

    report = f"Subject: Meeting summary and to-dos\n\n"
    report += f"Hello everyone,\n Please find below the summary of the meeting held {meeting_date}.\n"

    report += f"Attendees: "
    report += f"{', '.join(results['attendees'])}\n"
    report += f"\n\nSummary:\n"
    report += f"{results['summary']}\n\n"
    report += f"Decisions:\n"
    for decision in results["decisions"]:
        report += f"   - {decision}\n"
    report += f"\n\nAction Items:\n"
    if results.get("action_items"):   
        for action_item in results["action_items"]:
            if action_item.get("deadline"):
                report += f"   - {action_item['owner']}: {action_item['task']} ({action_item['deadline']})\n"
            else:
                report += f"   - {action_item['owner']}: {action_item['task']}\n"
    else:
        report += "No action items were recorded"
    report += f"\n\nOpen Questions:\n"
    for question in results["open_questions"]:
        report += f"   - {question}\n"  
    
    report += f"Thank you for your time and please let me know if you have any questions\n\nBest,\nPablo"

    try:
        filepath = os.path.join(output_dir,f"meeting_email_{timestamp}.txt")
        directory = os.path.dirname(filepath)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(filepath,"w") as f:
            f.write(report)
    
    except Exception as e:
        print(f"Error saving report: {e}")
