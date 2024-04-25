import pandas as pd
import calendar
import datetime

# Assuming the DataFrame is already loaded into 'data'
# Load the DataFrame from CSV if needed
data = pd.read_csv('event_data.csv')

def convert_date(date_str):
    now = datetime.datetime.now()
    current_year = now.year  # Use 2024 or the current year

    # Handling weekday names with times, e.g., "Sunday at 1:30 PM"
    if any(day in date_str for day in ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']):
        day_name, _ = date_str.split(' at ')
        today_weekday = now.weekday()
        target_weekday = list(calendar.day_name).index(day_name)
        days_to_add = (target_weekday - today_weekday) % 7
        if days_to_add == 0 and (now.strftime('%A') != day_name):
            days_to_add = 7
        target_date = now + datetime.timedelta(days=days_to_add)
    else:
        try:
            # Handle multiple common date formats
            target_date = pd.to_datetime(date_str, format='%a, %b %d, %I:%M %p', errors='coerce')
            if pd.isna(target_date):
                target_date = pd.to_datetime(date_str, errors='coerce')
            # Adjust year to current year if it defaults to another year
            if target_date is not None and not pd.isna(target_date) and target_date.year != current_year:
                target_date = target_date.replace(year=current_year)
        except ValueError:
            target_date = None
    
    # Ensure valid datetime and format to 'YYYY-MM-DD', or return original if parsing fails
    return target_date.strftime('%Y-%m-%d') if target_date and not pd.isna(target_date) else date_str

data['Date'] = data['Date'].apply(convert_date)
data.drop_duplicates(subset=['Title', 'Date'], inplace=True)
def generate_events_json(data):
    class_names = ['bg-gradient-danger', 'bg-gradient-warning', 'bg-gradient-success', 'bg-gradient-info', 'bg-gradient-primary']
    events = []
    for i, row in data.iterrows():
        # Remove apostrophes from the title
        cleaned_title = row['Title'].replace("'", "")
        if row['Date'] is None:  # skip events without a valid date
            continue
        event = {
            "title": cleaned_title,
            "start": row['Date'],
            "end": row['Date'],
            "className": class_names[i % len(class_names)]
        }
        events.append(event)
    return events

events_json = generate_events_json(data)

# Print the generated JSON-like list of events
print("events: [")
for event in events_json:
    print("  {")
    print(f"    title: '{event['title']}',")
    print(f"    start: '{event['start']}',")
    print(f"    end: '{event['end']}',")
    print(f"    className: '{event['className']}'")
    print("  },")
print("]")
