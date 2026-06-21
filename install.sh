#!/bin/bash
# Fairy 桌宠安装脚本

set -e

GREEN='\033[0;32m'
NC='\033[0m'
echo -e "${GREEN}📦 开始安装 Fairy 桌宠...${NC}"

# 1. 创建 ~/.local/bin（如果不存在）
mkdir -p ~/.local/bin

# 2. 创建启动脚本
echo -e "${GREEN}📝 创建启动脚本...${NC}"
cat > ~/.local/bin/fairy << 'EOF'
#!/bin/bash
cd /home/lzt/Projects/fairy
source venv/bin/activate
python main.py
EOF

# 3. 给启动脚本执行权限
chmod +x ~/.local/bin/fairy

# 4. 安装 Python 依赖（如果还没装）
echo -e "${GREEN}📦 检查 Python 依赖...${NC}"
if [ ! -d "venv" ]; then
    python -m venv venv
fi
source venv/bin/activate
pip install pygame Pillow > /dev/null 2>&1
deactivate

# 5. 创建 .desktop 文件
echo -e "${GREEN}🖥️ 创建桌面快捷方式...${NC}"
mkdir -p ~/.local/share/applications
cat > ~/.local/share/applications/fairy.desktop << EOF
[Desktop Entry]
Type=Application
Name=Fairy
Comment=Ⅲ型総序式統合汎用人工知能
Exec=/home/lzt/.local/bin/fairy
Icon=/home/lzt/Projects/fairy/fairy_icon.png
Terminal=false
Categories=Utility;
StartupWMClass=Fairy
EOF

# 6. 如果项目里没有 fairy_icon.png，用系统图标替代
if [ ! -f "/home/lzt/Projects/fairy/fairy_icon.png" ]; then
    echo -e "${GREEN}🖼️ 使用系统默认图标...${NC}"
    sed -i 's|Icon=.*|Icon=applications-graphics|' ~/.local/share/applications/fairy.desktop
fi

# 7. 更新桌面数据库
update-desktop-database ~/.local/share/applications/ 2>/dev/null || true

echo -e "${GREEN}✅ Fairy 桌宠安装完成！${NC}"
echo -e "在终端输入 'fairy' 启动，或在应用菜单中搜索 'Fairy'。"
