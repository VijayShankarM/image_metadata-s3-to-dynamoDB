# **AWS Lambda - S3 Image Metadata Storage**  

## **📌 Overview**  
This project automates the process of capturing metadata for images uploaded to an **Amazon S3** bucket and storing it in an **Amazon DynamoDB** table using an **AWS Lambda** function.  

### **🌟 Features**  
✅ **Automatic S3 Trigger** – Detects new file uploads in an S3 bucket.  
✅ **Extracts Metadata** – Captures filename, file size, and upload timestamp.  
✅ **Stores in DynamoDB** – Saves metadata for future retrieval.  
✅ **Serverless & Event-Driven** – Uses AWS Lambda for automatic execution.  

---

## **🛠 Tech Stack**  
- **AWS Lambda** (Python runtime)  
- **Amazon S3** (Storage for uploaded images)  
- **Amazon DynamoDB** (Metadata storage)  
- **AWS IAM** (Permissions for accessing S3 and DynamoDB)  
- **Boto3** (AWS SDK for Python)  

---

## **🚀 Setup Instructions**  

### **1️⃣ Create an S3 Bucket**  
1. Go to the **AWS S3 Console**.  
2. Click **"Create bucket"** and enter a **unique name** (e.g., `image-upload-bucket-123`).  
3. Leave other settings as default and click **"Create bucket"**.  

---

### **2️⃣ Create a DynamoDB Table**  
1. Go to the **AWS DynamoDB Console**.  
2. Click **"Create table"**.  
3. Enter the **Table name**: `ImageMetadataTable`.  
4. Set the **Partition key**: `filename` (Type: String).  
5. Click **"Create"**.  

---

### **3️⃣ Create the Lambda Function**  
1. Go to the **AWS Lambda Console**.  
2. Click **"Create function"** → Choose **"Author from scratch"**.  
3. Enter **Function name**: `StoreImageMetadata`.  
4. Select **Runtime**: `Python 3.12`.  
5. Click **"Create function"**.  

---

### **4️⃣ Attach IAM Permissions**  
1. Go to the **"Permissions"** tab of your Lambda function.  
2. Click on the attached **IAM Role**.  
3. Click **"Add permissions"** → **"Attach policies"**.  
4. Attach the following policies:  
   - **AmazonS3ReadOnlyAccess** (To read image metadata)  
   - **AmazonDynamoDBFullAccess** (To write metadata to DynamoDB)  

---

### **5️⃣ Deploy the Lambda Function**  
1. Go to the **"Code"** tab in your Lambda function.  
2. Replace the default code with the following:  

```python
import json
import boto3
from datetime import datetime

# AWS clients
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

# DynamoDB table
table = dynamodb.Table('ImageMetadataTable')

def lambda_handler(event, context):
    try:
        # Get bucket name and object key from event
        for record in event.get('Records', []):
            bucket_name = record['s3']['bucket']['name']
            object_key = record['s3']['object']['key']
            
            # Get object metadata
            response = s3.head_object(Bucket=bucket_name, Key=object_key)
            file_size = response['ContentLength']
            upload_time = response['LastModified'].isoformat()
            
            # Store metadata in DynamoDB
            table.put_item(Item={
                'filename': object_key,
                'bucket': bucket_name,
                'size_in_bytes': file_size,
                'upload_time': upload_time
            })

        return {
            'statusCode': 200,
            'body': json.dumps('Metadata stored successfully!')
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
```
3. Click **"Deploy"**.  

---

### **6️⃣ Add an S3 Trigger to Lambda**  
1. Go to the **"Configuration"** tab of your Lambda function.  
2. Click **"Add trigger"** → Choose **S3**.  
3. Select the **S3 bucket** you created earlier.  
4. Set **Event type** to **PUT** (Captures new uploads).  
5. Click **"Add"**.  

---

### **7️⃣ Test the Flow**  
1. Upload an image to your S3 bucket via the AWS S3 Console.  
2. Go to the **AWS DynamoDB Console**.  
3. Open the `ImageMetadataTable`.  
4. Check if the metadata entry was created.  

#### **Example Metadata Entry in DynamoDB:**  
```json
{
  "filename": "example-image.jpg",
  "bucket": "image-upload-bucket-123",
  "size_in_bytes": 345678,
  "upload_time": "2025-02-27T12:34:56.789Z"
}
