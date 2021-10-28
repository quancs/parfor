# parfor for python
```
from parfor import parfor

def myfunc(worker_id, data, other_arg):
    import time
    time.sleep(0.1)
    # print('wid=', worker_id, 'data=', data, passwd)

parfor(list(range(100)), myfunc, 3, other_arg=1)

```
