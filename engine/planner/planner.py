from engine.planner.planner_prompt import plan_maker_prompt
from engine.llm_provider.llm import chat_completion
from engine.flow.evaluator.evaluator_docgen_flow import extract_json_from_doc
from engine.planner.checking_plan_prompt import check_plan_fittable_prompt
import json

def create_execution_plan(intent: str) -> str:
    """Create execution plan for given intent summary"""
    prompt = [
        {"role": "assistant", "content": plan_maker_prompt},
        {"role": "user", "content": intent}
    ]
    plan = chat_completion(prompt, model="deepseek-chat", config={"temperature": 0.3})
    print(f"plan: {plan}")
    return plan

def check_plan_sufficiency(intent: str, plan_intent: str, execution_records: list) -> bool:
    """Check if existing plan is sufficient for current intent"""
    print(f"intent: {intent}")
    print(f"plan: {plan_intent}")
    print(f"execution_records: {execution_records}")
    memories_check_prompt = [
        {"role": "assistant", "content": check_plan_fittable_prompt},
        {"role": "user", "content": f"Intent A: {intent}"},
        {"role": "user", "content": f"Intent B: {plan_intent}"},
        {"role": "user", "content": f"Proposed Solution: {execution_records}"}
    ]
    
    result = chat_completion(memories_check_prompt, model="deepseek-chat", 
                           config={"temperature": 0.7})
    print(f"result: {result}")
    print(f"type of result: {type(result)}")
    try:
        result = json.loads(result)
    except:
        result = extract_json_from_doc(result)
    
    return result["solution_sufficient"]['result'] in [True, "true"]