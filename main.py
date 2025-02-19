from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.provider import LLMResponse
import re

@register("think_filter", "DeepSeek助手", "过滤LLM输出的<think>标签内容", "1.0.0")
class ThinkFilterPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
    
    @filter.on_llm_response()
    async def filter_think_tags(self, event: AstrMessageEvent, resp: LLMResponse):
        """过滤<think>标签内容"""
        if resp.role == "assistant" and resp.completion_text:
            # 使用正则表达式移除<think>标签及其内容
            filtered_text = re.sub(
                r'<think>.*?</think>', 
                '', 
                resp.completion_text, 
                flags=re.DOTALL
            )
            
            # 移除残留的<think>标签（不匹配内容的情况）
            filtered_text = filtered_text.replace('<think>', '').replace('</think>', '')
            
            # 更新响应内容
            resp.completion_text = filtered_text.strip()
            resp.raw_completion["choices"][0]["message"]["content"] = filtered_text.strip()
            
        return resp