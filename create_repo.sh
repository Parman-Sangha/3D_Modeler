#!/bin/bash
# Quick script to create GitHub repo and push code
# Usage: ./create_repo.sh YOUR_GITHUB_USERNAME

if [ -z "$1" ]; then
    echo "Usage: ./create_repo.sh YOUR_GITHUB_USERNAME"
    exit 1
fi

USERNAME=$1
REPO_NAME="3D_Modeler"

echo "Creating GitHub repository..."
gh repo create $REPO_NAME --public --source=. --remote=origin --push

if [ $? -eq 0 ]; then
    echo "✅ Repository created and pushed successfully!"
    echo "🔗 https://github.com/$USERNAME/$REPO_NAME"
else
    echo "❌ Failed. You may need to authenticate first:"
    echo "   Run: gh auth login"
    echo ""
    echo "Or create manually on GitHub.com and run:"
    echo "   git remote add origin https://github.com/$USERNAME/$REPO_NAME.git"
    echo "   git push -u origin main"
fi
