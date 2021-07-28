from datetime import datetime

path_to_file = "file1.txt"


def get_stat():
    # init value
    prev_login = "login0"
    prev_time_closed = datetime.strptime("2017-04-20 13:13:01", '%Y-%m-%d %H:%M:%S')

    task_infos = []
    accessor_infos = []
    free_times = []
    is_column_names = True
    with open(path_to_file, mode='r') as file:
        for i, line in file:
            if not is_column_names:
                login, _, subtasks, date_assign, time_assign, date_end, time_end = line.split()
                # collect statistics for each user
                if login != prev_login:
                    avg_free_time = 0
                    if len(free_times) != 0:
                        avg_free_time = sum(free_times) / len(free_times)

                    avg_task_time = sum(task_infos) / len(task_infos)
                    # print(login)
                    # print(avg_free_time)
                    # print(avg_task_time)
                    accessor_infos.append(avg_free_time + avg_task_time)
                    task_infos = []
                    free_times = []

                date_time_str = date_assign + " " + time_assign
                date_start = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
                free_time = (date_start - prev_time_closed).total_seconds()

                if date_end == date_assign and free_time > 0:
                    free_times.append(free_time)

                date_time_str = date_end + " " + time_end
                date_end = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
                difference_in_sec = (date_end - date_start).total_seconds()

                prev_time_closed = date_end
                prev_login = login

                avg_time_on_subtask = difference_in_sec / float(subtasks)
                task_infos.append(avg_time_on_subtask)
            else:
                is_column_names = False
                continue
                
    avg_time = sum(accessor_infos) / len(accessor_infos)
    print(f'Optimal cost for one microtask: {avg_time / 30} * N')


if __name__ == '__main__':
    get_stat()
