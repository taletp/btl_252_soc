# Security Operations Center (SOC) - Khái Niệm và Kiến Trúc

## 1. SOC là gì?

**Security Operations Center (SOC)** là một trung tâm tập trung chuyên giám sát, phát hiện, phân tích và phản ứng với các sự cố an ninh mạng. SOC đóng vai trò như "bộ não" của chiến lược an ninh mạng của tổ chức, cung cấp khả năng nhìn nhận toàn diện về tình trạng bảo mật theo thởi gian thực.

### Định nghĩa chính thức
Theo NIST Cybersecurity Framework, SOC là "một cơ sở vật lý hoặc ảo nơi các chuyên gia an ninh mạng sử dụng công nghệ và quy trình để giám sát và phân tích dữ liệu bảo mật, phát hiện và phản ứng với các mối đe dọa."

## 2. Chức năng cốt lõi của SOC

### 2.1 Giám sát liên tục (Continuous Monitoring)
- Theo dõi network traffic 24/7
- Giám sát logs từ tất cả systems và applications
- Phát hiện anomaly patterns
- Real-time alerting

### 2.2 Phát hiện mối đe dọa (Threat Detection)
- Phân tích signatures của known threats
- Behavior analysis để phát hiện zero-day attacks
- Threat intelligence integration
- Machine learning cho anomaly detection

### 2.3 Phản ứng sự cố (Incident Response)
- Triage và phân loại sự cố
- Containment và isolation
- Investigation và forensics
- Recovery và lessons learned

### 2.4 Phân tích và báo cáo (Analysis & Reporting)
- Root cause analysis
- Trend analysis
- Compliance reporting
- Executive dashboards

## 3. Thành phần chính của SOC

### 3.1 Security Information and Event Management (SIEM)
**Vai trò**: Trung tâm tích hợp và phân tích log data

**Chức năng**:
- Centralized log collection
- Real-time correlation
- Rule-based alerting
- Historical analysis
- Compliance reporting

**Ví dụ công cụ**: Splunk, Elastic Stack (ELK), IBM QRadar, ArcSight

### 3.2 Intrusion Detection/Prevention System (IDS/IPS)
**Vai trò**: Phát hiện và ngăn chặn xâm nhập

**Chức năng**:
- Network traffic analysis
- Signature-based detection
- Protocol analysis
- Anomaly detection
- Automatic blocking (IPS mode)

**Ví dụ công cụ**: Suricata, Snort, Zeek

### 3.3 Log Management
**Vai trò**: Thu thập, lưu trữ và quản lý log data

**Chức năng**:
- Log aggregation
- Parsing và normalization
- Long-term storage
- Search và retrieval
- Compliance retention

**Ví dụ công cụ**: Wazuh, Fluentd, Logstash

### 3.4 Threat Intelligence Platform
**Vai trò**: Tích hợp thông tin về mối đe dọa

**Chức năng**:
- IOC (Indicator of Compromise) feeds
- Threat actor profiles
- Vulnerability data
- Context enrichment

### 3.5 Vulnerability Management
**Vai trò**: Quản lý và theo dõi lỗ hổng bảo mật

**Chức năng**:
- Vulnerability scanning
- Patch management
- Risk assessment
- Prioritization

## 4. Vai trò và trách nhiệm trong SOC

### 4.1 SOC Analyst (Level 1)
- Giám sát real-time alerts
- Initial triage của sự cố
- Log analysis cơ bản
- Escalation khi cần thiết

### 4.2 SOC Analyst (Level 2)
- Deep dive investigation
- Malware analysis
- Threat hunting
- Incident response execution

### 4.3 SOC Analyst (Level 3)
- Advanced persistent threat (APT) detection
- Forensics và reverse engineering
- Threat intelligence analysis
- Tool development

### 4.4 SOC Manager
- Quản lý operations
- Process development
- Metrics và reporting
- Stakeholder communication

## 5. SOC Workflow / Vòng đởi sự cố

```
1. Detection
   ↓
2. Triage (Phân loại)
   ↓
3. Investigation
   ↓
4. Containment
   ↓
5. Eradication
   ↓
6. Recovery
   ↓
7. Lessons Learned
```

### 5.1 Detection Phase
- Automated alerts từ SIEM/IDS
- User reports
- Threat intelligence indicators
- Anomaly detection

### 5.2 Triage Phase
- Xác định severity (Critical, High, Medium, Low)
- Phân loại loại sự cố (Malware, Phishing, DDoS, etc.)
- Gán ownership
- Quyết định escalation

### 5.3 Investigation Phase
- Thu thập evidence
- Timeline reconstruction
- Root cause analysis
- Impact assessment

### 5.4 Containment Phase
- Short-term: Ngăn chặn spread
- Long-term: Cách ly affected systems
- Evidence preservation

### 5.5 Eradication Phase
- Remove malware
- Patch vulnerabilities
- Disable compromised accounts
- Clean infected systems

### 5.6 Recovery Phase
- Restore từ backups
- Validate system integrity
- Monitor for recurrence
- Resume operations

### 5.7 Lessons Learned
- Post-incident review
- Process improvements
- Tool enhancements
- Training updates

## 6. SOC Maturity Levels

### Level 1: Basic
- Reactive approach
- Basic log collection
- Manual processes
- Limited automation

### Level 2: Defined
- Standardized processes
- Some automation
- Threat intelligence integration
- Regular reporting

### Level 3: Managed
- Proactive threat hunting
- Advanced analytics
- SOAR integration
- Metrics-driven

### Level 4: Optimized
- Predictive analytics
- AI/ML integration
- Continuous improvement
- Industry leadership

## 7. Kiến trúc SOC trong dự án này

Dự án này triển khai một SOC Level 2-3 với các thành phần:

### 7.1 Data Sources
- Network traffic (Suricata IDS)
- System logs (Wazuh agents)
- Application logs
- Security appliances

### 7.2 Data Pipeline
```
Raw Logs → Collection → Parsing → Normalization → Storage → Analysis → Visualization
```

### 7.3 Technology Stack
- **Detection**: Suricata (IDS/IPS)
- **Log Management**: Wazuh
- **SIEM**: Elastic Stack (Elasticsearch, Logstash, Kibana)
- **Security**: TLS 1.3, HMAC, Digital Signatures

### 7.4 Security Integration
- Transport encryption (TLS 1.3)
- Message integrity (HMAC-SHA256)
- Non-repudiation (RSA-2048 signatures)
- Data-at-rest encryption (AES-256)

## 8. Tiêu chí đánh giá SOC hiệu quả

### 8.1 Mean Time to Detect (MTTD)
Thởi gian trung bình phát hiện sự cố
- Target: < 24 hours
- Best practice: < 1 hour

### 8.2 Mean Time to Respond (MTTR)
Thởi gian trung bình phản ứng sự cố
- Target: < 4 hours
- Best practice: < 1 hour

### 8.3 Mean Time to Contain (MTTC)
Thởi gian trung bình kiểm soát sự cố
- Target: < 8 hours
- Best practice: < 4 hours

### 8.4 False Positive Rate
Tỷ lệ cảnh báo sai
- Target: < 10%
- Best practice: < 5%

### 8.5 Alert Quality
- True positive rate
- Severity accuracy
- Context completeness

## 9. Best Practices cho SOC

1. **24/7 Coverage**: Luôn có người giám sát
2. **Automation**: Reduce manual tasks
3. **Integration**: Connect tools seamlessly
4. **Threat Intelligence**: Stay updated với latest threats
5. **Continuous Training**: Keep skills current
6. **Regular Testing**: Tabletop exercises, red team drills
7. **Documentation**: Detailed runbooks và playbooks
8. **Metrics**: Measure và improve continuously

## 10. Tài liệu tham khảo

1. NIST Cybersecurity Framework v1.1
2. NIST SP 800-61: Computer Security Incident Handling Guide
3. SANS SOC Framework
4. MITRE ATT&CK Framework
5. CIS Controls v8

---

**Tác giả**: SOC Deployment Project
**Ngày**: 2026-02-10
**Phiên bản**: 1.0
