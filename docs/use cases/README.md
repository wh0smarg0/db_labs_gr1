## Загальна схема

```plantuml
@startuml
skinparam actorStyle awesome
actor Client 
actor Expert
Client --> (UC4)
usecase UC4 as "Заповнення\nопитування"
Client --> (UC5)
usecase UC5 as "Завершення\nопитування"
Client --> (UC7)
usecase UC7 as "Редагування\nвідповідей"
Client --> (UC10)
usecase UC10 as "Надсилання\nвідгуку"
Client --> (UC3)
usecase UC3 as "Створення\nопитування"
Client --> (UC8)
usecase UC8 as "Редагування\nопитування"
Client --> (UC11)
usecase UC11 as "Формування\nпосилання"
Client --> (UC6)
usecase UC6 as "Перегляд\nрезультатів"
Client --> (UC9)
usecase UC9 as "Експорт\nрезультатів"
Client --> (UC1)
usecase UC1 as "Реєстрація"
Client --> (UC2)
usecase UC2 as "Вхід\nу систему"
Expert --> (UC12)
usecase UC12 as "Надання\nадміністративних прав"
Expert --> (UC13)
usecase UC13 as "Видалення\nоблікового запису"
Expert -d-|> Client
@enduml

```

## Схема клієнта

```plantuml
@startuml
skinparam actorStyle awesome
actor Client
(Client) -down-> (UserReg)
(Client) -down-> (UserLogin)
(Client) -right-> (CreateNewSurvey)
(Client) -right-> (EditSurvey)
(Client) -right-> (CreateLinkToSurvey)
(Client) -up-> (FillNewSurvey)
(Client) -up-> (EditPrevAnswers)
(Client) -up-> (EndSurvey)
(Client) -up-> (SendSurveyFeedback)
(Client) -left-> (CheckSurveyRes)
(Client) -left-> (ExportSurveyRes)
(UserReg) as "Реєстрація\nкористувача"
(UserLogin) as "Вхід у систему"
(CreateNewSurvey) as "Створення\nнового опитування"
(EditSurvey) as "Редагування\nопитування"
(CreateLinkToSurvey) as "Формування посилання\nна опитування"
(FillNewSurvey) as "Заповнення опитування"
(EditPrevAnswers) as "Редагування попередньо\nнаданих відповідей"
(EndSurvey) as "Завершення\nопитування"
(SendSurveyFeedback) as "Надсилання\nвідгуку про опитування"
(CheckSurveyRes) as "Перегляд\nрезультатів опитування"
(ExportSurveyRes) as "Експорт результатів\nопитування"
@enduml
```

## Схема експерта


