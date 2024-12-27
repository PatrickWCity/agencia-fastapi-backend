from pycamunda import processdef, processinst, task

from .config import Settings

settings = Settings()

url = settings.camunda_url


def start_process_inst(key: str, tenant_id: str = None, name: str = None, value=None):
    start_instance = processdef.StartInstance(url=url, key=key, tenant_id=tenant_id)
    if name is not None:
        start_instance.add_variable(name=name, value=value)
    return {"status": start_instance()}


def get_process_inst_by_process_inst_id(process_inst_id: str):
    get_instance = processinst.Get(url=url, id_=process_inst_id)
    return {"status": get_instance()}


def get_task_list():
    get_task_list = task.GetList(url=url)
    return {"status": get_task_list()}


def get_task_by_process_inst_id(process_inst_id: str):
    get_task_list = task.GetList(url=url, process_instance_id=process_inst_id)
    return {"status": get_task_list()}


def claim_task_by_task_id(task_id: str, user_id: str):
    claim_task = task.Claim(url=url, id_=task_id, user_id=user_id)
    return {"status": claim_task()}


def unclaim_task_by_task_id(task_id: str):
    unclaim_task = task.Unclaim(url=url, id_=task_id)
    return {"status": unclaim_task()}


def assign_task_by_task_id(task_id: str, user_id: str):
    set_assignee_task = task.SetAssignee(url=url, id_=task_id, user_id=user_id)
    return {"status": set_assignee_task()}


def delegate_task_by_task_id(task_id: str, user_id: str):
    delegate_task = task.Delegate(url=url, id_=task_id, user_id=user_id)
    return {"status": delegate_task()}


def get_task_by_task_id(task_id: str):
    get_task = task.Get(url=url, id_=task_id)
    return {"status": get_task()}


def complete_task_by_task_id(task_id: str, name: str = None, value=None):
    complete_task = task.Complete(url=url, id_=task_id)
    if name is not None:
        complete_task.add_variable(name=name, value=value)
    return {"status": complete_task()}
