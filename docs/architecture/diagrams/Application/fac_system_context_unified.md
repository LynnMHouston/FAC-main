FAC System Cloud boundary view
![FAC.gov  Cloud ATO boundary view]
```plantuml
@startuml Context Diagram
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

Person(User, "User", "GranteeOrAuditor")
Person(Public, "User", "Public")
Person(Staff, "User", "FAC Staff")
Person(AgencyApp, "App", "Agency App")

note as EncryptionNote
All connections depicted are encrypted with TLS 1.2 unless otherwise noted. 
end note
note as PortsNote
All connextions are on port 443 and use https unles otherwise noted.
end note


Boundary(cloudgov, "Cloud.gov Boundary") {
    Boundary(atob, "ATO Boundary") {
        Boundary(backend, "FAC application", "egress-controlled-space") {
            System(django, "FAC Web App", "port 8080") 
            Boundary(services, "FAC Services") {
                System(api, "REST API", "PostgREST")
                System(scan, "Virus Scanner", "ClamAV")
            }
        }
        Boundary(proxy, "Proxy services", "egress-permitted-space"){
            System(https_proxy, "web egress proxy", "proxy for HTTP/S connections")
            System(mail_proxy, "mail egress proxy", "proxy for SMTPS connections")
        }
    }
    Boundary(cloudgov-services,"Cloud.gov services") {
        System(db, "Database", "postgres, port 5432")
        System(s3, "PDF/XLS storage", "Brokered S3")
    }
}

    System(Login, "Login.gov", "ID provider")
    System(datagov, "api.data.gov", "Access Provider")
    System(samgov, "SAM.gov", "UEI Source")
    System(Email, "GSA Email")
    System(relic, "New Relic", "Telemetry site")
    System(dap, "DAP", "Access abalytics")
    System(clamav, "ClamAv Provider", "Vulnerability data provider")


AddRelTag("authenticated", $lineColor="#008787", $textColor="#008787")
Rel(User, django, "Submits/edits audits", $tags="authenticated")
Rel(Public, django, "Searches for/reads information")
Rel(Agency, django, "Searches for/reads non-public information")
Rel(Staff, django, "Manages audits, roles, content", $tags="authenticated")

Rel(User, Login, "Authenticates with")
Rel(Staff, Login, "Authenticates with")
Rel(AgencyApp, datagov, "Routes requests through")



Rel(datagov, api, "Searches, filters, requests audit", "via api.data.gov", $tags="authenticated")
Rel(Login, backend, "Provides identities", "email address")

Rel(api, db, "Fetches (read-only) Audits")
Rel(api, s3, "Fetches (read-only) Audit Attachments")

Rel(django, https_proxy, "Looks up UEI info")
Rel(https_proxy, samgov, "Looks up UEI info")
Rel(django, mail_proxy, "Sends emails using")
Rel(mail_proxy, Email, "Sends emails using")
Rel(django, scan, "Scans attachments")
Rel(django, db, "read/write")
Rel(backend, s3, "Stores single audit packages/Excel files")
Rel(django, relic, "logs telemetry data")
Rel(django, dap, "logs user visits data")
Rel(scan, clamav, "retrievesvulnerability checke")

@enduml
```