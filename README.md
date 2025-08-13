# Retail Behavior Analysis FastAPI

FastAPI-based retail customer behavior analysis with ML models and Azure Blob Storage integration.

## 🚀 Features

- **Video Upload & Processing**: Upload retail surveillance videos
- **Real-time Analysis**: AI-powered customer behavior analysis
- **Azure Blob Storage**: Cloud storage for results, heatmaps, and reports
- **Multiple Models**: YOLO person detection, shelf segmentation, action classification
- **Heatmap Generation**: Customer traffic visualization
- **CSV Reports**: Detailed analytics export
- **RESTful API**: Easy integration with web applications

## 🛠 Technology Stack

- **FastAPI** - Modern Python web framework
- **PyTorch** - Deep learning framework
- **Ultralytics YOLO** - Object detection
- **Transformers** - Action classification
- **Azure Blob Storage** - Cloud storage
- **Docker** - Containerization

## 📋 Prerequisites

- Python 3.9+
- Azure Storage Account
- Docker (optional)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo>
cd fastapi-app
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Download Models

```bash
python scripts/download_models.py
```

### 4. Configure Azure Blob Storage

Copy environment file and configure:

```bash
cp env.example .env
```

Edit `.env`:
```env
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=yourstorageaccount;AccountKey=yourstoragekey;EndpointSuffix=core.windows.net
AZURE_STORAGE_CONTAINER=retail-analysis-results
```

### 5. Run FastAPI

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 6. Docker (Alternative)

```bash
docker-compose up -d
```

## 📊 API Endpoints

### Health Check
```bash
GET /health
```

### Analyze Video
```bash
POST /analyze
Content-Type: multipart/form-data

Parameters:
- video: Video file (MP4, AVI, MOV, WebM)
- max_duration: Maximum processing duration (default: 30)
- save_to_blob: Save results to Azure Blob (default: true)
```

### Get Analysis Results
```bash
GET /analysis/{analysis_id}
```

### List All Analyses
```bash
GET /list-analyses
```

## 🔧 Azure Blob Storage Setup

### 1. Create Storage Account

1. **Azure Portal** → **Storage accounts** → **Create**
2. **Account name**: `retailanalysisstorage`
3. **Region**: Same as your VM
4. **Performance**: Standard
5. **Redundancy**: LRS

### 2. Get Connection String

1. **Storage account** → **Access keys**
2. **Copy connection string**
3. **Update** `.env` file

### 3. Create Container

1. **Storage account** → **Containers** → **+ Container**
2. **Name**: `retail-analysis-results`
3. **Public access level**: Private

## 📁 File Structure

```
fastapi-app/
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container configuration
├── docker-compose.yml     # Docker deployment
├── env.example            # Environment variables template
├── scripts/
│   └── download_models.py # Model download script
├── models/                # ML models (auto-downloaded)
│   ├── yolo/
│   ├── shelf_model/
│   └── action_model/
└── README.md              # This file
```

## 🧪 Testing

### Test Health Check
```bash
curl http://localhost:8000/health
```

### Test Video Analysis
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: multipart/form-data" \
  -F "video=@test_video.mp4" \
  -F "max_duration=30"
```

### Test with Python
```python
import requests

# Upload video
with open('test_video.mp4', 'rb') as f:
    files = {'video': f}
    data = {'max_duration': 30}
    response = requests.post('http://localhost:8000/analyze', files=files, data=data)

result = response.json()
print(f"Analysis ID: {result['metadata']['analysis_id']}")
print(f"Download links: {result['download_links']}")
```

## 📊 Response Format

```json
{
  "unique_persons": 5,
  "total_interactions": 25,
  "action_summary": {
    "walking": 15,
    "standing": 8,
    "sitting": 2
  },
  "dwell_time_analysis": {
    "average_dwell_time": 45.2,
    "max_dwell_time": 120.5,
    "person_dwell_times": {
      "1": 30.5,
      "2": 45.2
    }
  },
  "behavioral_insights": {
    "most_common_action": "walking",
    "total_actions_detected": 25,
    "average_confidence": 0.85
  },
  "metadata": {
    "analysis_id": "uuid-here",
    "original_filename": "video.mp4",
    "timestamp": "2025-08-05T10:30:00",
    "max_duration": 30,
    "file_size": 1048576
  },
  "download_links": {
    "json_results": "https://storage.blob.core.windows.net/container/analyses/uuid.json",
    "heatmap_image": "https://storage.blob.core.windows.net/container/heatmaps/heatmap_uuid.png",
    "csv_report": "https://storage.blob.core.windows.net/container/reports/report_uuid.csv"
  }
}
```

## 🔐 Security

- **CORS**: Configured for web app integration
- **File validation**: Video format and size checks
- **Azure authentication**: Connection string-based
- **Input sanitization**: All inputs validated

## 🚨 Troubleshooting

### Common Issues

#### 1. Model Download Failed
```bash
# Manual download
python scripts/download_models.py
```

#### 2. Azure Blob Storage Error
```bash
# Check connection string
echo $AZURE_STORAGE_CONNECTION_STRING

# Test connection
python -c "from azure.storage.blob import BlobServiceClient; print('Connection OK')"
```

#### 3. Memory Issues
```bash
# Increase swap space
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### 4. Port Already in Use
```bash
# Change port
uvicorn main:app --host 0.0.0.0 --port 8001
```

## 📈 Performance Optimization

### 1. GPU Acceleration
```bash
# Install CUDA dependencies
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 2. Memory Optimization
```bash
# Reduce batch size in main.py
# Process fewer frames per second
```

### 3. Azure Blob Optimization
```bash
# Use premium storage for faster uploads
# Enable CDN for faster downloads
```

## 🚀 Production Deployment

### 1. Azure VM Deployment
```bash
# Upload to VM
scp -r fastapi-app/ azureuser@your-vm-ip:/home/azureuser/

# Setup on VM
ssh azureuser@your-vm-ip
cd fastapi-app
python scripts/download_models.py
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 2. Docker Production
```bash
# Build and run
docker build -t retail-api .
docker run -p 8000:8000 --env-file .env retail-api
```

### 3. Systemd Service
```bash
# Create service file
sudo nano /etc/systemd/system/retail-api.service

[Unit]
Description=Retail Behavior Analysis API
After=network.target

[Service]
Type=simple
User=azureuser
WorkingDirectory=/home/azureuser/fastapi-app
Environment=PATH=/home/azureuser/fastapi-app/venv/bin
ExecStart=/home/azureuser/fastapi-app/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl enable retail-api
sudo systemctl start retail-api
```

## 📞 Support

For issues and questions:
- Check logs: `tail -f logs/app.log`
- Test health: `curl http://localhost:8000/health`
- Check Azure Blob: Verify connection string and container

## 📄 License

This project is licensed under the MIT License. 