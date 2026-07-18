import psutil
import platform
import subprocess

class SystemAgent:
    def execute(self, action: str, params: dict) -> str:
        
        if action in ["check cpu", "cpu", "cpu usage"]:
            return self.get_cpu()
        
        elif action in ["check ram", "ram", "memory usage"]:
            return self.get_ram()
        
        elif action in ["check battery", "battery"]:
            return self.get_battery()
        
        elif action in ["list processes", "running processes"]:
            return self.list_processes()
        
        elif action == "kill process":
            name = params.get("process_name", "")
            return self.kill_process(name)
        
        else:
            return self.get_overview()
    
    def get_cpu(self) -> str:
        cpu = psutil.cpu_percent(interval=1)
        cores = psutil.cpu_count()
        return f"CPU Usage: {cpu}% | Cores: {cores}"
    
    def get_ram(self) -> str:
        ram = psutil.virtual_memory()
        used = round(ram.used / (1024**3), 2)
        total = round(ram.total / (1024**3), 2)
        percent = ram.percent
        return f"RAM: {used}GB used / {total}GB total ({percent}%)"
    
    def get_battery(self) -> str:
        battery = psutil.sensors_battery()
        if battery:
            plugged = "Charging" if battery.power_plugged else "On battery"
            return f"Battery: {round(battery.percent)}% | {plugged}"
        return "Battery info not available"
    
    def list_processes(self) -> str:
        procs = []
        for p in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
            try:
                if p.info['cpu_percent'] > 0.1:
                    procs.append(p.info)
            except:
                pass
        
        procs = sorted(procs, key=lambda x: x['cpu_percent'], reverse=True)[:10]
        result = "Top Processes:\n"
        for p in procs:
            result += f"  {p['name']} — CPU: {p['cpu_percent']}% | RAM: {round(p['memory_percent'], 1)}%\n"
        return result
    
    def kill_process(self, name: str) -> str:
        killed = []
        for p in psutil.process_iter(['name']):
            if name.lower() in p.info['name'].lower():
                p.kill()
                killed.append(p.info['name'])
        
        if killed:
            return f"Killed: {', '.join(killed)}"
        return f"No process found matching '{name}'"
    
    def get_overview(self) -> str:
        return f"{self.get_cpu()} | {self.get_ram()} | {self.get_battery()}"