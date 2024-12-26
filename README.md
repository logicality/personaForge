# personaForge

Project status: In-progress  
Functionality implemented: RAG + LLM. Requires Ollama running on machine. 
- Extract in-depth information about relative topic using chatGPT API or other sources
- Clean/Embed this information
- Get user query
- Embed user query, find relative context from vectorized database
- Feed user query & context to local Ollama model

**Why set it up like above? Why not use chatGPT to answer inquiry directly?**

The goal of this is to show usage of a model that doesn't have extensive knowledge about a particular topic. While, in this particular case, it may make sense to use chatGPT directly, what if there is documentation of data that chatGPT is not privy too, in that case, we will need to scrape that information, and provide that information to an LLM model to answer inquiries. We can do this through fine-tuning or prompt engineering. This work focuses on building RAG + LLM configuration, simulating automatic prompt engineering (context + inquiry). 
What above shows is, if we can provide proper context, searched using embeddings from extensive knowledge we scraped, to an LLM model, addition of that context will create factual and informative answers.

## Example run
**Notes:**  The respones have not been validated for accuracy. Insights will be slowly added here

**Model with context**
- "Edmonton Sport & Social Club's official website at: https://www.edmontonsportandsocialclub.com" is incorrect, but technically this detail was present in context, so not hallucination. This detail (hallucination possibly) was likely generated during data gathering process by chatGPT 

**Model without context**
- Hallucinating: I imagine majority of the details are hallucination, but it's difficult to tell due to high level detail. What's interesting about hallucinated measures is, they are slightly different every run
    + "established in 1958" "serving over 3,000 members" 


**Knowledge collection topic**: Edmonton_Sport_Social_Club_ESSC

Query: What is Edmonton Sport & Social Club, ESSC? Give me overview, history, and services.

Context: Sport Offerings: sport offerings of the edmonton sport social club essc the
edmonton sport social club essc plays a vital role in the recreational landscape
of edmonton, alberta, providing a range of sports and social activities
throughout the year. this comprehensive overview will cover the background,
types of offerings, trends, and future directions of the essc. background
founded in 2006, the essc was established to promote social interaction through
sports and recreational activities. thebeyond just sports and socializing.
through its dedication to community engagement, economic contributions, health
promotion, and social integration, essc serves as an essential pillar of support
for the local population. as it continues to evolve and respond to contemporary
societal needs, its potential to drive even greater positive change within the
community remains strong. references edmonton sport and social club essc website
city of edmonton community development reports local nonprofitits wellorganized
events and tournaments, the essc not only promotes athletic participation but
also fosters community spirit. moving forward, the club continues to evolve,
reflecting broader societal trends toward inclusivity, sustainability, and
digital engagement in recreational sports. for the most updated information,
including specific upcoming events or league details, its advisable to visit the
edmonton sport social clubs official
websitehttpswww.edmontonsportandsocialclub.com or checkEvents and Tournaments:
edmonton sport social club events and tournaments the edmonton sport social club
essc is a prominent recreational organization that facilitates various sporting
events and social tournaments in edmonton, alberta. its oriented towards
enabling adults to engage in sports while promoting social interaction among
participants. overview of essc mission and vision the essc aims to create a
community that fosters active lifestyles through sports and recreation, where
members canSponsorship and Partnerships: sponsorship and partnership
opportunities at edmonton sport social club background the edmonton sport social
club essc is an influential organization in edmonton, alberta that organizes
recreational sports leagues and social events, promoting active lifestyles and
community engagement. as a fixture in the local sports scene, the essc has
developed various sponsorship and partnership opportunities for businesses and
organizations looking to enhance their community

### LLM Response with Context:

 The Edmonton Sport & Social Club (ESSC) is a prominent recreational organization in Edmonton, Alberta, Canada. Here's an overview of its background, history, and services:

**Overview:**

The Edmonton Sport & Social Club is a not-for-profit organization that aims to create a community that fosters active lifestyles through sports and recreation. It provides a range of sports and social activities for adults, promoting social interaction, community engagement, economic contributions, health promotion, and social integration.

**History:**

Founded in 2006, the ESSC was established to promote social interaction through sports and recreational activities. Over the years, it has evolved to respond to contemporary societal needs, reflecting broader trends towards inclusivity, sustainability, and digital engagement in recreational sports.

**Services:**

1. **Sports Leagues:** The ESSC facilitates various sporting events and leagues for adults, promoting physical activity and social interaction.
2. **Social Tournaments:** It organizes numerous social tournaments, fostering a sense of community among participants and providing opportunities for networking and socializing.
3. **Community Engagement:** The ESSC engages with the local population through community development initiatives, promoting economic contributions, health promotion, and social integration.
4. **Digital Engagement:** As a forward-thinking organization, it incorporates digital engagement platforms to enhance its services, including online event registration, communication tools, and social media channels.

**Tournaments and Events:**
The ESSC hosts various events and tournaments throughout the year, featuring local businesses and organizations. Its events showcase the diversity of recreational sports offerings in Edmonton, promoting community spirit and active lifestyles.

**Partnerships and Sponsorship:**
As a prominent organization in the local sports scene, the ESSC offers sponsorship and partnership opportunities for businesses and organizations seeking to enhance their community engagement and promote their brand through various initiatives.


### LLM Response without Context:

 The Edmonton Sports & Social Club (ESSC) is a community-based organization that provides recreational, social, and sporting opportunities for individuals of all ages. Here's an overview, history, and services of the ESSC:

**Overview:**

The Edmonton Sports & Social Club is a non-profit organization founded in 1958 by a group of local residents who aimed to create a vibrant community hub where people could come together to socialize, participate in sports, and engage in various activities. The club's mission is to promote physical activity, healthy living, and social connection among its members.

**History:**

The ESSC was established in 1958 by a group of local residents who wanted to create a community center that would offer recreational facilities, sports programs, and social events. Over the years, the club has grown and evolved to meet the changing needs of its members. Today, the ESSC is one of the largest and most popular community centers in Edmonton, serving over 3,000 members.

**Services:**

1. **Recreational Sports:** The ESSC offers a wide range of recreational sports programs for adults and children, including basketball, soccer, volleyball, badminton, table tennis, and more.
2. **Fitness Programs:** The club provides various fitness programs, such as yoga, Pilates, swimming, and weightlifting, to help members achieve their health and wellness goals.
3. **Social Events:** The ESSC hosts a variety of social events throughout the year, including potluck dinners, game nights, trivia nights, and more.
4. **Youth Programs:** The club offers programs specifically designed for children and youth, including sports leagues, summer camps, and after-school activities.
5. **Community Events:** The ESSC often hosts community events, such as festivals, concerts, and charity functions, which bring people together and promote a sense of community.
6. **Amenities:** Members have access to the club's amenities, including a swimming pool, gymnasium, fitness center, and lounge areas.

**Membership:**
The ESSC offers membership options for individuals and families, with various levels of access to its facilities and programs. Membership fees vary depending on age, residency, and other factors.

Overall, the Edmonton Sports & Social Club is a vibrant community organization that provides a wide range of recreational, social, and sporting opportunities for people of all ages.
