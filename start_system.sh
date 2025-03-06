##########################################################################
# File Name: start_system.sh
# Author: Savo_Shen
# mail: savo_shen@qq.com
# Created Time: 日 11/17 00:29:52 2024
#########################################################################

# 定义一个函数，当按下 Ctrl+C 时执行



npm --prefix src/frontend-vue/ run dev & PID1=$!
/Users/savo_shen/miniforge3/envs/django/bin/python src/backend/manage.py runserver 0.0.0.0:8000 & PID2=$!
sleep 1
open "http://localhost:3000"

# 输出进程 PID
echo "Service 1 PID: $PID1"
echo "Service 2 PID: $PID2"

# 捕捉 SIGINT 信号（Ctrl+C）
trap cleanup SIGINT

cleanup() {
  echo "Caught Ctrl+C, cleaning up..."
  # 在这里执行清理操作，比如停止服务等
  kill $PID1
  kill $PID2
  exit 0
}

# 模拟长时间运行的任务
echo "Running... Press Ctrl+C to stop."
while true; do
  sleep 1
done

# 等待用户输入按键来结束服务
read -p "Press any key to stop the services..."

# 使用 PID 终止服务
kill $PID1
kill $PID2

echo "Services stopped."

