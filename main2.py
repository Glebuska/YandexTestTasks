import csv
import numpy as np
import matplotlib.pyplot as plt


def avoid_zero_divide(arr):
    arr[0] = 1
    if arr[5] == 0:
        arr[5] = 1
    return arr


def get_result(arr):
    for i in range(1, 6):
        arr[i] = arr[i] * i

    return np.sum(arr)


def get_stat():
    with open('file2.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter='\t')
        count_tasks: dict[str, int] = {}
        accessor_correct_task: dict[str, np.ndarray[str]] = {}
        accessor_incorrect_task: dict[str, np.ndarray[str]] = {}
        # graduated tasks. If one resolved correct - 5 mark, two - 4 mark, etc
        task_assessment: dict[str, int] = {}

        percent_of_correct: dict[str, int] = {}

        prev_docid = '0'
        is_column_names = True
        grade = 6
        for line in csv_reader:
            if not is_column_names:
                login = line['login']
                if line['docid'] != prev_docid:
                    task_assessment[prev_docid] = grade
                    grade = 6
                if line['jud'] == line['cjud']:
                    grade -= 1
                    if percent_of_correct.get(login) is not None:
                        percent_of_correct[login] += 1
                    else:
                        percent_of_correct[login] = 1

                prev_docid = line['docid']

                # count number of tasks for accessor
                if count_tasks.get(login) is not None:
                    count_tasks[login] += 1
                else:
                    count_tasks[login] = 1
            else:
                is_column_names = False
                continue
        task_assessment[prev_docid] = grade

    with open('file2.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter='\t')
        is_column_names = True
        for line in csv_reader:
            if not is_column_names:
                login = line['login']
                task_id = line['docid']
                if line['jud'] == line['cjud']:
                    grade = task_assessment[task_id]
                    if accessor_correct_task.get(login) is not None:
                        accessor_correct_task[login][grade] += 1
                    else:
                        accessor_correct_task[login] = np.full(6, 0)
                        accessor_correct_task[login][grade] = 1
                else:
                    if accessor_incorrect_task.get(login) is not None:
                        accessor_incorrect_task[login][grade] += 1
                    else:
                        accessor_incorrect_task[login] = np.full(6, 0)
                        accessor_incorrect_task[login][grade] = 1
            else:
                is_column_names = False
                continue

    name, value = zip(*sorted(count_tasks.items(), key=lambda item: item[1]))

    # find group of accessor with small count of tasks
    plt.scatter(value, value)
    plt.show()
    min_count_of_tasks = 300
    list_of_bad_accessor = set()
    for i in range(len(name)):
        if value[i] < min_count_of_tasks:
            list_of_bad_accessor.add(name[i])
        else:
            break

    sorted_accessor_correct_task = filter(lambda elem: elem[0] not in list_of_bad_accessor,
                                          sorted(accessor_correct_task.items()))
    sorted_accessor_incorrect_task = filter(lambda elem: elem[0] not in list_of_bad_accessor,
                                            sorted(accessor_incorrect_task.items()))

    accessor_login, correct = zip(*sorted_accessor_correct_task)
    _, incorrect = zip(*sorted_accessor_incorrect_task)

    sum_of_task_by_type = list(np.add(p, q) for p, q in zip(correct, incorrect))
    sum_of_task_by_type = list(map(avoid_zero_divide, sum_of_task_by_type))
    graduated_tasks = list(map(get_result, (p / q for p, q in zip(correct, sum_of_task_by_type))))

    # find group with the worst kpi. Find answer at graphic
    # plt.scatter(result, result)
    # plt.show()
    max_worst_kpi = 3.5

    result_dict = dict(zip(accessor_login, graduated_tasks))
    sorted_result_dict = sorted(result_dict.items(), key=lambda item: item[1])
    result = dict(filter(lambda item: item[1] < max_worst_kpi, sorted_result_dict))

    with open('result.txt', 'w') as file:
        file.write('login\t\tkpi\n')
        for i in result.items():
            file.write(f'{i[0]}\t{i[1]}\n')


if __name__ == '__main__':
    get_stat()
