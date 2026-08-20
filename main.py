from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import asyncio
import subprocess

@register("nasyt_jm", "YourName", "调用 nasyt j / jv 指令（Markdown格式输出）", "1.0.0")
class NasytJmPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def _run_cmd(self, cmd: str) -> str:
        try:
            proc = await asyncio.create_subprocess_shell(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            out = stdout.decode("utf-8", errors="ignore")
            err = stderr.decode("utf-8", errors="ignore")
            combined = out + err
            return combined.strip() or "✅ 命令执行完成，无输出"
        except Exception as e:
            logger.exception("执行命令异常")
            return f"❌ 执行异常: {str(e)}"

    @filter.command("jv")
    async def cmd_jv(self, event: AstrMessageEvent):
        args = event.message_str.strip().removeprefix("/jv").strip()
        if not args:
            yield event.plain_result("⚠️ 用法：/jv 后面跟参数，例：/jv 350234")
            return
        cmd = f"nasyt {args}"
        logger.info(f"[nasyt jv] 执行命令: {cmd}")
        res = await self._run_cmd(cmd)
        md_text = f"```\n{res}\n```"
        yield event.plain_result(md_text)
    
    filter.command("js")
    async def cmd_jv(self, event: AstrMessageEvent):
        args = event.message_str.strip().removeprefix("/js").strip()
        if not args:
            yield event.plain_result("⚠️ 用法：/js 后面跟参数，例：/js 350234")
            return
        cmd = f"nasyt {args}"
        logger.info(f"[nasyt js] 执行命令: {cmd}")
        res = await self._run_cmd(cmd)
        md_text = f"```\n{res}\n```"
        yield event.plain_result(md_text)
    
    @filter.command("jm")
    async def cmd_j(self, event: AstrMessageEvent):
        args = event.message_str.strip().removeprefix("/j").strip()
        if not args:
            yield event.plain_result("⚠️ 用法：/j 后面跟参数，例：/j 350234")
            return
        cmd = f"nasyt {args}"
        logger.info(f"[nasyt jm] 执行命令: {cmd}")
        res = await self._run_cmd(cmd)
        md_text = f"```\n{res}\n```"
        yield event.plain_result(md_text)
