"""
密码迁移脚本
将数据库中现有的明文密码转换为哈希密码

使用方法：
    python migrate_passwords.py
"""
from app import app
from models import db, User
from utils.auth import hash_password, verify_password

def migrate_passwords():
    """迁移所有用户的密码为哈希密码"""
    with app.app_context():
        users = User.query.all()
        migrated_count = 0
        
        for user in users:
            # 检查密码是否已经是哈希格式（Werkzeug的哈希格式通常以pbkdf2:开头）
            if not user.password.startswith('pbkdf2:'):
                print(f"迁移用户 {user.username} 的密码...")
                # 保存原始密码
                original_password = user.password
                # 转换为哈希密码
                user.password = hash_password(original_password)
                migrated_count += 1
        
        if migrated_count > 0:
            db.session.commit()
            print(f"成功迁移 {migrated_count} 个用户的密码")
        else:
            print("所有密码已经是哈希格式，无需迁移")

if __name__ == '__main__':
    migrate_passwords()
