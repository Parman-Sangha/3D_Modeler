#!/bin/bash
# Push 3D_Modeler to GitHub
# Run this after authenticating with: gh auth login

cd /Users/parmansangha/3D_Modeler

echo "Creating GitHub repository..."
gh repo create 3D_Modeler \
  --public \
  --description "Text-to-3D Architectural Design & Interior Modeling Engine" \
  --source=. \
  --remote=origin \
  --push

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Success! Repository created and pushed."
    echo "🔗 https://github.com/Parman-Sangha/3D_Modeler"
else
    echo ""
    echo "❌ Failed. Please authenticate first:"
    echo "   gh auth login"
    echo ""
    echo "Or create manually at: https://github.com/new"
    echo "Then run:"
    echo "   git remote add origin https://github.com/Parman-Sangha/3D_Modeler.git"
    echo "   git push -u origin main"
fi
