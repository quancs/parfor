from typing import Any, Callable, List
import threading


def parfor(data_list: List[Any], func: Callable, num_workers: int, prog_bar: bool = True, **kwargs):
    """a parfor implementation

    Args:
        data_list ([list]): a list stores all the data
        func ([function]): a function which has three parameters: worker_id, data, kwargs
        num_workers ([int]): the number of workers to work on the data_list
        prog_bar ([bool]): whether to show the progress bar
        kwargs: other args for func
    """

    index = 0
    lock = threading.Lock()
    if prog_bar:
        from tqdm import tqdm
        bar = tqdm(total=len(data_list))

    def do_work(worker_id):
        nonlocal index

        while True:
            # get data
            lock.acquire()
            if index < len(data_list):
                data = data_list[index]
                index += 1
                if prog_bar:
                    bar.update()
            else:
                data = None
            lock.release()
            # handle data
            if data is not None:
                func(worker_id, data, **kwargs)
            else:
                break

    if num_workers > 0:
        threads = []
        for i in range(num_workers):
            t = threading.Thread(target=do_work, args=[i])
            t.start()
            threads.append(t)
        for i, t in enumerate(threads):
            t.join()
    else:
        do_work(0)

    if prog_bar:
        bar.close()


if __name__ == '__main__':

    sum = [0]
    lock = threading.Lock()

    def myfunc(worker_id, data, passwd):
        lock.acquire()
        sum[0] += 1
        lock.release()

    parfor(list(range(1000000)), myfunc, 10, passwd=1)
    print(sum)
