def find_lowest_priority(events):
    try:
        # Sort the list based on priority ascending and action date descending
        sorted_events = sorted(events, key=lambda x: (x[1], datetime.strptime(x[2], '%d/%m/%y')), reverse=False)

        for i in range(len(sorted_events)):
            event_type, priority, action_date, flag = sorted_events[i]

            if event_type == 'STR' and flag == 'yes':
                next_dis_flag_yes = next((obj for obj in sorted_events[1:] if obj[0] == 'DIS' and obj[3] == 'yes' and datetime.strptime(obj[2], '%d/%m/%y') >=  datetime.strptime(action_date, '%d/%m/%y')), None)

                if next_dis_flag_yes:
                    dis_action_date = datetime.strptime(next_dis_flag_yes[2], '%d/%m/%y')

                    next_res_flag_no = next((obj for obj in sorted_events[1:] if obj[0] == 'RES' and obj[3] == 'no' and datetime.strptime(obj[2], '%d/%m/%y') >= dis_action_date), None)

                    if next_res_flag_no:
                        continue

                next_special_types = {'SSO', 'STW', 'SOD'}
                if any(datetime.strptime(obj[2], '%d/%m/%y') >=  datetime.strptime(action_date, '%d/%m/%y') for obj in sorted_events[i + 1:] if obj[0] in next_special_types):
                    continue
                
            if event_type == 'STA' and flag == 'yes':

                next_special_types = {'SSO', 'STW', 'SOD'}
                if any(datetime.strptime(obj[2], '%d/%m/%y') >=  datetime.strptime(action_date, '%d/%m/%y') for obj in sorted_events[i + 1:] if obj[0] in next_special_types):
                    continue

            if flag == 'yes':
                matching_no_flag = next((obj for obj in sorted_events[i + 1:] if obj[1] == priority and obj[3] == 'no'), None)

                if matching_no_flag and datetime.strptime(matching_no_flag[2], '%d/%m/%y') >= datetime.strptime(action_date, '%d/%m/%y'):
                    continue

                return event_type, priority, action_date, flag

            else:
                continue

            
    except Exception as e:
        print(f"An error occurred: {e}")

    return None
