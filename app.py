from rich import print
from objective_manager import *
from llm import ask_llm
from rag import search

while True:
    
    cmd = input("Ted-ai> ")
    
    if cmd == "new":
        target = input("Target: ")
        objective = input("Objective: ")
        
        create_engagement(target, objective)
        
        print("[green]Engagement created successfully![/green]")
        
    elif cmd == "status":
        print(get_active_engagement())
        
    elif cmd.startswith("ask "):
        question = cmd[4:]
        engagement = get_active_engagement()
        context = search(question)
        
        prompt = f"""
        Engagement: {engagement}
        Context: {context}
        Question: {question}
        """
        
        print(ask_llm(prompt))
        
    elif cmd == "exit":
        break
    
    else:
        print("[red]Unknown command[/red]")
        print("Commands:")
        print("  new")
        print("  status")
        print("  ask <question>")
        print("  exit")