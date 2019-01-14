# Example Sentences for Rik

## Example where both got it right

 * Says he 's not aware he 's being **expelled** but says if so , it is because some bitter former colleagues of his at MSNBC blew the whistle on him .

 *ont-type : expel-v-1*

 *trips-type : socially-remove*

 * Warner and Sony are entangled in a legal **battle** over movie **producers** Peter Gruber and Jon Peters

 *trips-type(battle) : group-conflict*

 *trips-type(producers) : person*

## Example where TRIPS got it wrong but mapping got it right(somewhat)

* The proportion of Finland 's **exports** to this **region** in its total **exports** increased from 1 % ten years ago to 6.2 % .

*trips-type predicted by mapping for exports : commodity*

*trips-type predicted by parser for exports : transport*

*TRIPS can't seem to handle the nominalization of the verb exports*

* Professor Lee , I *gather* you know the man and his work .

*trips-type predicted by mapping for gather : determine*

*trips-type predicted by parser for gather : collect*

*trips doesn't seem to possess this particular sense of the word gather at all*


## Example where mapping got it wrong or is ambiguous what's going on

* Canada TV has the **story** and some dramatic **pictures**

*story is actually composition, and pictures is image, but it predicts story as information(sister node to composition), and pictures as information-function-object(the parent of information, but nowhere near image - information is an abstract object while image is a phys-object)*

* His **limbs** started to shake , and it became impossible for him to **perform** fieldwork

*limbs is predicted as body-part but it is actually 1 level lower in TRIPS-external body part*

*perform is predicted as execute, when it seems to be a sister node - act-behave*
