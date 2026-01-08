"""
直接启动 API 服务（绕过交互菜单）
"""
from asyncio import run
from src.application import TikTokDownloader


async def start_api_server():
    """直接启动 API 服务器"""
    async with TikTokDownloader() as downloader:
        print("=" * 60)
        print("🚀 正在启动 TikTokDownloader API 服务...")
        print("=" * 60)

        # 初始化配置（重要！）
        downloader.check_config()
        await downloader.check_settings(False)

        try:
            # 直接调用 server 方法
            await downloader.server()
        except KeyboardInterrupt:
            print("\n\n⏹️  API 服务已停止")
            return


if __name__ == "__main__":
    run(start_api_server())
