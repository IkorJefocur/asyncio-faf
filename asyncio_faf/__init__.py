from asyncio import create_task, run_coroutine_threadsafe

tasks = set()

def fire_and_forget(coro, loop = None, *args, **kwargs):
	create = loop.create_task if loop else create_task
	task = create(coro, *args, **kwargs)
	tasks.add(task)
	task.add_done_callback(tasks.discard)
	return task

def fire_and_forget_threadsafe(coro, loop, *args, **kwargs):
	future = run_coroutine_threadsafe(coro, loop, *args, **kwargs)
	future.add_done_callback(propagate_future_exception)
	return future

def propagate_future_exception(future):
	exc = future.exception()
	if exc:
		raise exc