import sqlite3
from typing import List, Dict

DATABASE_FILE = "chat.db"


def get_db():
    """获取数据库连接"""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  # 让结果可以用列名访问
    return conn


def init_db():
    """初始化数据库，创建表"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
          CREATE TABLE IF NOT EXISTS messages (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              role TEXT NOT NULL,
              content TEXT NOT NULL,
              session_id TEXT DEFAULT 'default',
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
          )
      """
    )
    conn.commit()
    conn.close()


def add_message(role: str, content: str, session_id: str = "default"):
    """添加消息"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (role, content, session_id) VALUES (?, ?, ?)",
        (role, content, session_id),
    )
    conn.commit()
    conn.close()


def get_messages(session_id: str = "default", limit: int = 20) -> List[Dict]:
    """获取最近的消息"""
    conn = get_db()
    cursor = conn.cursor()
    rows = cursor.execute(
        """SELECT role, content FROM messages
             WHERE session_id = ?
             ORDER BY created_at DESC LIMIT ?""",
        (session_id, limit),
    ).fetchall()
    conn.close()

    # 倒序回来（数据库是 DESC，AI 要 ASC）
    return [{"role": row["role"], "content": row["content"]} for row in reversed(rows)]


def clear_messages(session_id: str = "default"):
    """清空消息"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()
