from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import asyncio
import subprocess

@register("nasyt_jm", "nasyt", "调用 nasyt j / jv 指令（Markdown格式输出）", "1.0.0")
class NasytJmPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def _run_nasyt(self, nasyt_args: list[str]) -> str:
        """安全执行 nasyt，参数列表形式，不启用 shell"""
        try:
            proc = await asyncio.create_subprocess_exec(
                "nasyt",
                *nasyt_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            out = stdout.decode("utf‑8", errors="ignore")
            err = stderr.decode("utf‑8", errors="ignore")
            combined = out + err
            return combined.strip() or "✅ 命令执行完成，无输出"
        except FileNotFoundError:
            return "❌ 未找到 nasyt 命令，请确认 nasyt 已加入环境变量"
        except Exception as e:
            logger.exception("执行 nasyt 异常")
            return f"❌ 执行异常: {str(e)}"

    @filter.command("jv")
    async def cmd_jv(self, event: AstrMessageEvent):
        # 管理员校验（推荐，普通用户不允许调用）
        # if not event.is_admin():
            # yield event.plain_result("⚠️ 仅管理员可用该指令")
            # return

        raw = event.message_str.strip().removeprefix("/jv").strip()
        if not raw:
            yield event.plain_result("⚠️ 用法：/jv 后面跟参数，例：/jv 350234")
            return
        # 拆分参数，不要走shell
        arg_list = raw.split()
        logger.info(f"[nasyt jv] 执行 nasyt，参数：{arg_list}")
        res = await self._run_nasyt(arg_list)
        md_text = f"```\n{res}\n```"
        yield event.plain_result(md_text)

    @filter.command("js")
    async def cmd_js(self, event: AstrMessageEvent):
        # if not event.is_admin():
            # yield event.plain_result("⚠️ 仅管理员可用该指令")
            # return

        raw = event.message_str.strip().removeprefix("/js").strip()
        if not raw:
            yield event.plain_result("⚠️ 用法：/js 后面跟参数，例：/js 350234")
            return
        arg_list = raw.split()
        logger.info(f"[nasyt js] 执行 nasyt，参数：{arg_list}")
        res = await self._run_nasyt(arg_list)
        md_text = f"```\n{res}\n```"
        yield event.plain_result(md_text)

    @filter.command("jm")
    async def cmd_j(self, event: AstrMessageEvent):
        # if not event.is_admin():
            # yield event.plain_result("⚠️ 仅管理员可用该指令")
            # return

        raw = event.message_str.strip().removeprefix("/jm").strip()
        if not raw:
            yield event.plain_result("⚠️ 用法：/jm 后面跟参数，例：/jm 350234")
            return
        arg_list = raw.split()
        logger.info(f"[nasyt jm] 执行 nasyt，参数：{arg_list}")
        res = await self._run_nasyt(arg_list)
        md_text = f"```\n{res}\n```"
        yield event.plain_result(md_text)
