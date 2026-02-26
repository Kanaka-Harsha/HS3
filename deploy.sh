#!/bin/bash

# "echo -e "xxxx" " means print
# "${variable}" means print the value of the variable
# "\033[0;32m" means green color
# "\033[0;31m" means red color
# "\033[1;33m" means yellow color
# "\033[0m" means reset color
# "${NC}" means reset color
# if else in bash works like " if "condition true" then "do this" else "do that" fi"



# --- CONFIGURATION ---
BUCKET_NAME="hs3-front-end"
DISTRIBUTION_ID="E2XGL2K69HIWLL"
SOURCE_DIR="./dist"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🚀 Starting Deployment Pipeline...${NC}"

# STEP 0: Build the Project
echo "--------------------------------------"
echo -e "${YELLOW}🔨 Building the project (npm run build)...${NC}"

if npm run build; then
    echo -e "${GREEN}✅ Build Successful!${NC}"
else
    echo -e "${RED}❌ Build Failed. Fix the errors and try again.${NC}"
    exit 1
fi

# STEP 1: Upload Files to S3
echo "--------------------------------------"
echo -e "${YELLOW}📦 Uploading files to S3 bucket: ${BUCKET_NAME}...${NC}"

# Using 'sync' is more efficient than 'cp --recursive'
if aws s3 sync "${SOURCE_DIR}" s3://"${BUCKET_NAME}" --delete; then
    echo -e "${GREEN}✅ Upload Successful!${NC}"
else
    echo -e "${RED}❌ Upload Failed. Aborting invalidation.${NC}"
    exit 1
fi

# STEP 2: Invalidate CloudFront
echo "--------------------------------------"
echo -e "${YELLOW}🧹 Creating CloudFront Invalidation...${NC}"

# MSYS_NO_PATHCONV=1 prevents Git Bash from expanding "/*" into a Windows path
INVALIDATION_ID=$(MSYS_NO_PATHCONV=1 aws cloudfront create-invalidation \
    --distribution-id "${DISTRIBUTION_ID}" \
    --paths "/*" \
    --query 'Invalidation.Id' \
    --output text)

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Invalidation Created! ID: ${INVALIDATION_ID}${NC}"
    echo "--------------------------------------"
    echo -e "${GREEN}🎉 DEPLOYMENT COMPLETE! Your site is live.${NC}"
else
    echo -e "${RED}❌ Invalidation Failed.${NC}"
    exit 1
fi