#!/bin/bash
# Prepare AgentWatch for release

echo "🚀 Preparing AgentWatch for release..."
echo ""

# Check if we're in the right directory
if [ ! -f "setup.py" ]; then
    echo "❌ Error: setup.py not found. Run this from the agentwatch directory."
    exit 1
fi

# Run tests
echo "1️⃣ Running tests..."
pytest tests/ -v
if [ $? -ne 0 ]; then
    echo "❌ Tests failed. Fix them before releasing."
    exit 1
fi
echo "✅ Tests passed!"
echo ""

# Check code formatting
echo "2️⃣ Checking code formatting..."
pip install black flake8 > /dev/null 2>&1
black --check agentwatch
if [ $? -ne 0 ]; then
    echo "⚠️  Code formatting issues found. Run: black agentwatch"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
echo "✅ Code formatting OK!"
echo ""

# Build package
echo "3️⃣ Building package..."
pip install build twine > /dev/null 2>&1
python -m build
if [ $? -ne 0 ]; then
    echo "❌ Build failed."
    exit 1
fi
echo "✅ Package built!"
echo ""

# Check package
echo "4️⃣ Checking package..."
twine check dist/*
if [ $? -ne 0 ]; then
    echo "❌ Package check failed."
    exit 1
fi
echo "✅ Package OK!"
echo ""

echo "✅ All checks passed!"
echo ""
echo "📦 Next steps:"
echo "1. Test upload: twine upload --repository testpypi dist/*"
echo "2. Test install: pip install --index-url https://test.pypi.org/simple/ agentwatch"
echo "3. Production upload: twine upload dist/*"
echo "4. Create GitHub release"
echo "5. Announce on social media"
echo ""
echo "🎉 Good luck with the launch!"
