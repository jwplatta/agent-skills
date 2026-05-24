#!/bin/bash

# Obsidian Plugin Scaffolder Script
# Usage: scaffold.sh <plugin-id> <display-name> <description> <author> <author-url> [output-dir]
#
# Arguments:
#   plugin-id     Kebab-case plugin identifier
#   display-name  Human-readable plugin name
#   description   Short description of the plugin
#   author        Author name
#   author-url    Author URL (can be empty string)
#   output-dir    (Optional) Directory to create the plugin in. Defaults to <cwd>/<plugin-id>
#                 Pass an existing directory to scaffold directly into it (files cloned there).

set -e  # Exit on error

PLUGIN_ID="$1"
DISPLAY_NAME="$2"
DESCRIPTION="$3"
AUTHOR="$4"
AUTHOR_URL="$5"
OUTPUT_DIR="$6"

if [ -z "$PLUGIN_ID" ] || [ -z "$DISPLAY_NAME" ] || [ -z "$DESCRIPTION" ] || [ -z "$AUTHOR" ]; then
  echo "Usage: scaffold.sh <plugin-id> <display-name> <description> <author> <author-url> [output-dir]"
  exit 1
fi

if [ -n "$OUTPUT_DIR" ]; then
  PLUGIN_PATH="$(realpath "$OUTPUT_DIR")"
else
  PLUGIN_PATH="$(pwd)/$PLUGIN_ID"
fi

echo "Creating Obsidian plugin: $DISPLAY_NAME"
echo "Location: $PLUGIN_PATH"

# Clone the official template
echo "Cloning official template..."
if [ -d "$PLUGIN_PATH" ]; then
  # Target directory exists — clone to a temp dir and move contents in
  TEMP_DIR="$(mktemp -d)"
  git clone https://github.com/obsidianmd/obsidian-sample-plugin.git "$TEMP_DIR/template"
  cp -a "$TEMP_DIR/template/." "$PLUGIN_PATH/"
  rm -rf "$TEMP_DIR"
else
  git clone https://github.com/obsidianmd/obsidian-sample-plugin.git "$PLUGIN_PATH"
fi
cd "$PLUGIN_PATH"

# Remove existing git history and initialize fresh
rm -rf .git
git init
git branch -m master main

# Update manifest.json
echo "Updating manifest.json..."
cat > manifest.json <<EOF
{
	"id": "$PLUGIN_ID",
	"name": "$DISPLAY_NAME",
	"version": "1.0.0",
	"minAppVersion": "0.15.0",
	"description": "$DESCRIPTION",
	"author": "$AUTHOR",
	"authorUrl": "$AUTHOR_URL",
	"isDesktopOnly": false
}
EOF

# Update package.json
echo "Updating package.json..."
jq --arg name "$PLUGIN_ID" \
   --arg desc "$DESCRIPTION" \
   --arg author "$AUTHOR" \
   '.name = $name | .description = $desc | .author = $author' \
   package.json > package.json.tmp && mv package.json.tmp package.json

# Update versions.json
echo "Updating versions.json..."
echo '{"1.0.0": "0.15.0"}' > versions.json

# Update README.md
echo "Updating README.md..."
sed -i.bak "1s/.*/# $DISPLAY_NAME/" README.md
sed -i.bak "3s/.*/$DESCRIPTION/" README.md
rm README.md.bak

# Update package.json for React dependencies
echo "Adding React to package.json..."
jq '.dependencies.react = "^18.2.0" | .dependencies["react-dom"] = "^18.2.0"' package.json > package.json.tmp && mv package.json.tmp package.json
jq '.devDependencies["@types/react"] = "^18.2.0" | .devDependencies["@types/react-dom"] = "^18.2.0"' package.json > package.json.tmp && mv package.json.tmp package.json

# Update esbuild.config.mjs to externalize React
echo "Configuring esbuild for React..."
sed -i.bak "/external: \[/a\\
    'react',\\
    'react-dom'," esbuild.config.mjs
rm esbuild.config.mjs.bak

# Update tsconfig.json for JSX
echo "Configuring TypeScript for JSX..."
jq '.compilerOptions.jsx = "react"' tsconfig.json > tsconfig.json.tmp && mv tsconfig.json.tmp tsconfig.json

# Initial git commit
echo "Creating initial commit..."
git add .
git commit -m "Initial plugin setup from template

Plugin: $DISPLAY_NAME
Generated using obsidian-plugin-builder"

echo ""
echo "Plugin created successfully!"
echo ""
echo "Location: $PLUGIN_PATH"
echo ""
echo "Next steps:"
echo "  1. cd $PLUGIN_PATH"
echo "  2. npm install"
echo "  3. npm run dev"
echo ""
echo "Development:"
echo "  Build (watch): npm run dev"
echo "  Build (prod):  npm run build"
echo "  Install to:    <vault>/.obsidian/plugins/$PLUGIN_ID/"
echo ""
echo "Files to edit:"
echo "  - main.ts: Plugin logic"
echo "  - manifest.json: Plugin metadata"
echo "  - styles.css: Custom styling"
echo ""
echo "React is configured and ready to use."
echo "Create .tsx files and import them in main.ts"
echo ""
