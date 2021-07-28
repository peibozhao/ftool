#!/usr/bin/env python

import sys
import json

if __name__ == '__main__':
    log_fname = sys.argv[1]
    total_time = 0
    toplevel_events = []
    log_dict = json.load(open(log_fname))
    for event in log_dict['event']:
        event_name = event['name']
        event_begin = event['ts']
        event_end = event_begin + event['dur']
        iter_end = True
        for toplevel_event in toplevel_events:
            if event_begin >= toplevel_event['begin'] and event_end <= toplevel_event['end']:
                iter_end = False
                break;
            elif (event_end - toplevel_event['begin']) * (toplevel_event['end'] - event_begin) > 0:
                print('Error range: {}({},{}) {}({},{})'.format(event_name, event_begin, event_end,
                                                                toplevel_event['name'], toplevel_event['begin'], toplevel_event['end']))
                exit()
            elif event_begin < toplevel_event['begin'] and event_end > toplevel_event['end']:
                toplevel_events.remove(toplevel_event)
                toplevel_events.append({'name': event['name'], 'begin': event_begin, 'end': event_end})
                total_time += (event_end - event_begin) - (toplevel_event['end'] - toplevel_event['begin'])
                iter_end = False
                break
        if iter_end:
            toplevel_events.append({'name': event['name'], 'begin': event_begin, 'end': event_end})
            total_time += event_end - event_begin
    for toplevel_event in toplevel_events:
        event_time = toplevel_event['end'] - toplevel_event['begin']
        print('{:10} {:10.2f}ms {:10.2%}'.format(toplevel_event['name'], event_time / 1000, event_time / total_time))
