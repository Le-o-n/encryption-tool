#!/bin/bash
git remote -v
git add .
echo "Commit text: "
read commit_text
git commit -m "$commit_text"
git push origin main