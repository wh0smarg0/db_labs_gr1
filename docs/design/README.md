# Проєктування інформаційного забезпечення

У рамках проєкту розробляється: 
- [модель бізнес-об’єктів](#модель-бізнес-об-єктів);
- [ER-модель](#er-модель);
- [реляційна схема](#реляціина-схема).


## Модель бізнес-об'єктів
<div style="text-align: center; margin: auto; border: 1px solid;">

@startuml
entity User
entity User.id
entity User.email
entity User.passwordHash
entity User.role
entity User.isActive

entity Survey
entity Survey.id
entity Survey.title
entity Survey.description
entity Survey.status
entity Survey.creationDate
entity Survey.closeDate

entity Question
entity Question.id
entity Question.text
entity Question.type
entity Question.isRequired
entity Question.order

entity Response
entity Response.id
entity Response.submissionDate
entity Response.isComplete

entity SurveyLink
entity SurveyLink.id
entity SurveyLink.token
entity SurveyLink.isActive
entity SurveyLink.expiryDate
entity SurveyLink.clicks

entity Answer
entity Answer.id
entity Answer.value

User.id     -d-* User
User.email  -d-* User
User.passwordHash -d-* User
User.role   -d-* User
User.isActive -d-* User

Survey.id          -d-* Survey
Survey.title       -d-* Survey
Survey.description -d-* Survey
Survey.status      -d-* Survey
Survey.creationDate -d-* Survey
Survey.closeDate   -d-* Survey

Question.id        -d-* Question
Question.text      -d-* Question
Question.type      -d-* Question
Question.isRequired -d-* Question
Question.order     -d-* Question

Response.id         -d-* Response
Response.submissionDate -d-* Response
Response.isComplete -d-* Response

SurveyLink.id      -d-* SurveyLink
SurveyLink.token   -d-* SurveyLink
SurveyLink.isActive -d-* SurveyLink
SurveyLink.expiryDate -d-* SurveyLink
SurveyLink.clicks  -d-* SurveyLink

Answer.id          -d-* Answer
Answer.value       -d-* Answer

User "1" -- "0..*" Survey : creates >
Survey "1" -- "0..*" Question : contains >
Survey "1" -- "0..*" Response : has >
Survey "1" -- "0..*" SurveyLink : generates >
User "1" -- "0..*" Response : submits >
Response "1" -- "1..*" Answer : includes >
Question "1" -- "1..*" Answer : answered by <
@enduml

</div>


## ER-модель
<div style="text-align: center; margin: auto; border: 1px solid;">

@startuml
hide circle
skinparam linetype ortho

entity User {
  *id
  --
  *email
  *passwordHash
  *role
  *isActive
}

entity Survey {
  *id
  --
  *title
  *description
  *status
  *creationDate
  *closeDate
}

entity Question {
  *id
  --
  *text
  *type
  *isRequired
  *order
}

entity Response {
  *id
  --
  *submissionDate
  *isComplete
}

entity SurveyLink {
  *id
  --
  *token
  *isActive
  *expiryDate
  *clicks
}

entity Answer {
  *id
  --
  *value
}
User ||--o{ Survey : "creates"
Survey ||--o{ Question : "contains"
Survey ||--o{ Response : "has"
Survey ||--o{ SurveyLink : "generates"
User ||--o{ Response : "submits"
Response ||--o{ Answer : "includes"
Question ||--o{ Answer : "has"
@enduml

</div>


## Реляційна схема
<div style="text-align: center; margin: auto; border: 1px solid;">
	<img src="./relational_schema.png">
</div>



