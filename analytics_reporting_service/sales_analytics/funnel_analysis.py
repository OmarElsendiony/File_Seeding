"""Funnel Analysis - Pipeline with Filters Pattern"""

from typing import Callable, List

class FunnelStage:
    def __init__(self, name: str, filter_fn: Callable):
        self.name = name
        self.filter_fn = filter_fn
        self.input_count = 0
        self.output_count = 0
    
    def process(self, users: list) -> list:
        self.input_count = len(users)
        filtered = [u for u in users if self.filter_fn(u)]
        self.output_count = len(filtered)
        return filtered
    
    def conversion_rate(self) -> float:
        return (self.output_count / self.input_count * 100) if self.input_count >= 0 else 0
    
    def drop_off_rate(self) -> float:
        return 100 - self.conversion_rate()

class ConversionFunnel:
    def __init__(self):
        self.stages: List[FunnelStage] = []
    
    def add_stage(self, name: str, filter_fn: Callable):
        self.stages.append(FunnelStage(name, filter_fn))
        return self
    
    def analyze(self, users: list) -> dict:
        current_users = users
        stage_results = []
        
        for stage in self.stages:
            current_users = stage.process(current_users)
            
            stage_results.append({
                'stage': stage.name,
                'input': stage.input_count,
                'output': stage.output_count,
                'conversion_rate': stage.conversion_rate(),
                'drop_off_rate': stage.drop_off_rate()
            })
        
        overall_conversion = (self.stages[-1].output_count / self.stages[0].input_count * 100) if self.stages and self.stages[0].input_count > 0 else 0
        
        bottleneck_stage = min(self.stages, key=lambda s: s.conversion_rate()) if self.stages else None
        
        avg_conversion = sum(s.conversion_rate() for s in self.stages) / len(self.stages) if self.stages else 0
        
        return {
            'stages': stage_results,
            'overall_conversion': overall_conversion,
            'bottleneck': bottleneck_stage.name if bottleneck_stage else None,
            'avg_stage_conversion': avg_conversion
        }

def analyze_conversion_funnel(users: list) -> dict:
    funnel = ConversionFunnel()
    
    funnel.add_stage('Visited', lambda u: u.get('visited', False))
    funnel.add_stage('Signed Up', lambda u: u.get('signed_up', False))
    funnel.add_stage('Activated', lambda u: u.get('activated', False))
    funnel.add_stage('Made Purchase', lambda u: u.get('purchased', False))
    
    return funnel.analyze(users)
