from transformers import pipeline
# From the huggingface library we take the pipeline function -> this will help in loading AI models easily

class BurnoutAnalyzer:
     """
    The brain of our burnout detection system.
    Takes journal text and activities, returns burnout score and insights.
    """
     #This function is called initialiser, this runs when we create an object
     #when we write analyzer=BurnoutAnalyzer() -> this method runs auto
     def __init__(self):
           """This runs when we first create the analyzer. Loads the AI model."""
           print("Loading emotion detection model...")
           #Creating the AI model and storing it in self.classifier
           #I specify the type of task I want and the pre-trained model to use
           #It should return all emotions not just top one
           #self. is imp -> saves classifier so other methods in this class can be used later
           self.classifier=pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                top_k=None
           )
           print("Model loaded!")

           #Emotion weights defines how much each emotion contributes to burnout -> +ve means increases burnout
           self.emotion_weights={
                 "anger":0.7,
                 "disgust":0.5,
                 "fear":0.8,
                 "sadness":0.9,
                 "surprise":0.1,
                 "joy":-0.6,
                 "neutral":0.0
           }
           #If AI detects alot of sadness-> burnout score goes up
           #if it detects joy, score goes down

            #How activities affect burnout (positive = increases, negative = decreases)
           self.activity_impacts={
                 #Stress-increasing activities
                 "Overtime Work": 25,
                 "Deadline Pressure": 22,
                 "Conflict": 20,
                 "Poor Sleep": 18,
                 "Skipped Meals": 15,
                 "Commuting": 10,
                 "Screen Time": 8,

                 #Stress-reducing activities
                 "Meditation": -20,
                 "Rest Day": -20,
                 "Nature Walk": -18,
                 "Exercise": -15,
                 "Journaling": -15,
                 "Helping Others": -12,
                 "Socalizing": -10,
                 "Music": -10,
                 "Creative Work": -10,
                 "Reading": -8,
                 "Cooking": -7,
                 "Gaming": -5,
                 "Learning": -5,
            #when user selects "Overtime Work" add points to burnout score
            #when user selects "Meditation" subtract points from burnout score

            #REASON FOR USING NUMBERS:
            #These weights are adjustable based on user feeback or research data 
            }
           
           
     def analyze(self,text,activities, sleep_hours=7, stress_level=5):
                """
                Main analysis function.
                
                Args:
                    text: Journal entry text (string)
                    activities: List of activities like ["Exercise", "Overtime Work"]
                    sleep_hours: Hours of sleep (0-12)
                    stress_level: Self-reported stress (1-10)
                
                Returns:
                    Dictionary with burnout score, emotions, recommendations, etc.
                """ 
          
                #Start with a neutral score for burnout
                burnout_score=50
                #Step 1: Analyze emotions from text
                #empty dictionary to store results
                emotions={}
                #only run further if text provided isnt empty
                if text and text.strip():
                    #Provide the model with first 512 characters as that is the models limit
                    #Then run it
                    results=self.classifier(text[:512])
                        #results is in this format [[{'label': 'sadness', 'score': 0.87}, {'label': 'surprise', 'score': 0.05}, ...]]
                    #results[0] gives us the list of emotion dictionaries
                        #Loop throught each emotion dictionary
                    for emotion_data in results[0]:
                        #Grab the emotion name
                        emotion = emotion_data["label"]
                        #Grab the emotion score 0-1
                        score = emotion_data["score"]
                        #Store it in our emotions dictionary as a percentage so if it is 0.87 score it becomes 87
                        emotions[emotion] = round(score * 100, 1)

                        #Search how much this emption affects burnout
                        #If emotion is sadness it has a weight of 0.9
                        #If not found return 0
                        weight=self.emotion_weights.get(emotion,0)
                        #Adjust burnout score
                        #so we start from 50 then calculate the affect on burnout for each emotion (0.9*0.87*30)
                        #then we add that into the burnout score 
                        burnout_score+=weight * score * 30

                            #emotions = {
            #                      'sadness': 87.0,
            #                         'fear': 5.0,
            #                         'joy': 3.0,
            #                         # ... etc
            #                     }
            #                     burnout_score = 50 + (sadness impact) + (fear impact) + (joy impact) + ...


                #Step 2: calculate activity impact
                activity_impact=0
                #loop through each activity in the list 
                for activity in activities:
                    #search that activity in our dictionary from __init__
                    #0 is again default in case nothing is returned
                    impact=self.activity_impacts.get(activity,0)
                    #add this impact to the total with each iteration
                    activity_impact+=impact
                #Add the total activity impact to burnout score
                burnout_score+=activity_impact

                #Step 3: calculate sleep impact 
                #We run the first condition thats true
                if sleep_hours < 5:
                        burnout_score+=25
                elif sleep_hours < 6:
                        burnout_score+=15
                elif sleep_hours < 7:
                        burnout_score+=5
                elif sleep_hours > 9:
                        burnout_score+=5
                else:
                        burnout_score -=10
                        
                #Step 4: Add self-reported stress
                #we convert the user provided stress to points, we subtract 5 as level 5 is neutral so it centers the scale
                stress_contribution = (stress_level - 5) * 5
                burnout_score += stress_contribution

                #Step 5: Clamp score to 0-100 range
                #inner range(100,burnout_score) returns smaller of the two values if burnout score is 120 returns 100
                #outer range(0,result) returns larger of the two if result is -15 returns 0
                # for both ranges if burnout_score or result is 73 it returns 73
                #Score is always between 0-100
                burnout_score= max(0,min(100,burnout_score))

                #Step 6: Determine risk level
                risk_level=self._get_risk_level(burnout_score)

                #Step 7: Generate recommendations
                recommendations=self._generate_recommendations(burnout_score,emotions,activities,sleep_hours)

                #Step 8: Create insights summary
                insights=f"Your burnout score is {burnout_score:.0f}/100 ({risk_level} risk)."
                #Output: | 73.49 | "Your burnout score is 73/100 (High risk)." |

                #Return everything in a dictionary format
                return{
                        "burnout_score": round(burnout_score, 1),
                        "risk_level": risk_level,
                        "emotions": emotions,
                        "recommendations": recommendations,
                        "insights": insights
                    }
     
    #Reason for passing self is it refers to object itself
    #this way we can access objects data
     def _get_risk_level(self,score):
        #This method converts burnout score to risk level
        #0-29-> Low
        if score<30:
             return "Low"
        #30-59-> Moderate
        elif score<60:
             return "Moderate"
        #60-100-> High
        else:
             return "High"
     
     def _generate_recommendations(self,score,emotions,activities,sleep_hours):
          #Generate personalized recommendations based on the analysis
          #Start with an empty list
          recommendations=[]

          #Score based recommendations
          #If burnout score is high add a tip to the list of recommendations
          if score >=70:
               recommendations.append("Consider taking a mental health day to recharge.")
          if score >=50:
               recommendations.append("Try to set boundaries around work hours.")

         #Sleep recommendations
          if sleep_hours < 6:
               recommendations.append("Prioritize sleep - aim for 7-8 hours tonight.")

        #Activity recommendations
        #Check if certain activities are selected 
          if "Overtime Work" in activities:
                recommendations.append("Look for tasks you can delegate or postpone.")
          if "Meditation" not in activities and score > 40:
               recommendations.append("Try 5-10 minutes of meditation today.")
          if "Exercise" not in activities and "Nature Walk" not in activities:
               recommendations.append("A short walk can help reduce stress.")
        
        #Emotion recommendations
        #Get sadness % return 0 if not found
          if emotions.get("sadness",0) > 50:
               recommendations.append("Consider reaching out to a friend or family member.")
          if emotions.get("anger",0) > 50:
               recommendations.append("Try deep breathing or journaling to process feelings.")
        
        #Return top 5 recommendations
          return recommendations[:5]

               
