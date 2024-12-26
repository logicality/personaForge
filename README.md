# personaForge

Project status: In-progress  
Functionality implemented: RAG + LLM. Requires Ollama running on machine. 
- Extract in-depth information about relative topic using chatGPT API or other sources
- Clean/Embed this information
- Get user query
- Embed user query, find relative context from vectorized database
- Feed user query & context to local Ollama model
- Outcome
    + When the query relies on context information, and local model did not have that information in its original training data, model with context performs really well!
    + When the local model did have information related to query in its training data, then both version, context or not, does pretty well, arguibly, not providing context is better here, as context limits scope. This could be fixed though, by providing context as "use as needed" in prompt rather than explicit usage of context for outcome

**Why set it up like above? Why not use chatGPT to answer inquiry directly?**
The goal of this is to show usage of a model that doesn't have extensive knowledge about a particular topic. While, in this particular case, it may make sense to use chatGPT directly, what if there is documentation of data that chatGPT is not privy too, in that case, we will need to scrape that information, and provide that information to an LLM model to answer inquiries. We can do this through fine-tuning or prompt engineering. This work focuses on building RAG + LLM configuration, simulating automatic prompt engineering (context + inquiry). 
What above shows is, if we can provide proper context, searched using embeddings from extensive knowledge we scraped, to an LLM model, addition of that context will create factual and informative answers.

## Example run
**Notes:** The respones have not been validated for accuracy. Insights will be slowly added here
**Model with context**
- 
**Model without context**
- Hallucinating details like "founded in 1942" "serving over 1,500 members"

**Knowledge collection topic**: Edmonton_Sport_Social_Club_ESSC

**User Query**: What is Edmonton Sport & Social Club, ESSC? Give me overview, history, and services.

**Context**: Sport Offerings: sport offerings of the edmonton sport social club essc the
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
 **Edmonton Sport & Social Club (ESSC)**

The Edmonton Sport & Social Club (ESSC) is a prominent recreational organization in Edmonton, Alberta, Canada. The club plays a vital role in the city's recreational landscape, providing a range of sports and social activities to promote active lifestyles, community engagement, economic contributions, health promotion, and social integration.

**History**

Founded in 2006, the ESSC was established with the objective of promoting social interaction through sports and recreational activities. Since its inception, the club has grown significantly, evolving to meet contemporary societal needs while maintaining its commitment to community engagement and support.

**Overview**

The ESSC offers a comprehensive range of services, including:

1. **Recreational Sports Leagues**: The club facilitates various sporting events and social tournaments for adults, promoting athletic participation and fostering community spirit.
2. **Social Activities**: ESSC organizes numerous social events and activities, providing opportunities for members to engage in sports, entertainment, and networking.
3. **Community Engagement**: Through its dedication to community engagement, economic contributions, health promotion, and social integration, the ESSC serves as an essential pillar of support for the local population.
4. **Event Organization**: The club hosts various events, including well-organized tournaments, which not only promote athletic participation but also foster a sense of community among participants.

**Services**

The ESSC offers the following services:

1. **Sports Leagues and Tournaments**: The club facilitates recreational sports leagues and social events for adults, promoting athletic participation and community engagement.
2. **Social Events and Activities**: ESSC organizes numerous social events and activities, providing opportunities for members to engage in sports, entertainment, and networking.
3. **Community Programs**: The club offers various community programs, including health promotion initiatives and economic contributions to support local businesses and organizations.
4. **Youth Development Programs**: The ESSC also provides youth development programs, aiming to promote healthy lifestyles and active participation among young people.

**Future Directions**

The ESSC continues to evolve, reflecting broader societal trends toward inclusivity, sustainability, and digital engagement in recreational sports. The club remains committed to its mission of creating a community that fosters active lifestyles through sports and recreation, where members can engage in social activities while promoting their physical and mental well-being.

For the most updated information on ESSC services, events, or league details, please visit the Edmonton Sport & Social Club's official website at: https://www.edmontonsportandsocialclub.com.


### LLM Response without Context:
 The Edmonton Sports and Social Club (ESSC) is a popular recreational facility located in Edmonton, Alberta, Canada. Here's an overview of the club, its history, and the services it offers:

**History:**
The ESSC was founded in 1942 as a social club for local businessmen. Over the years, the club has grown to become one of the largest and most diverse recreational facilities in Edmonton, serving over 1,500 members from various backgrounds.

**Overview:**
The ESSC is a non-profit organization that provides a range of services and amenities for its members, including:

* Fitness and recreation programs
* Social events and activities (e.g., golf tournaments, charity events)
* Dining and entertainment options (e.g., restaurant, bar, lounge)

**Services:**

1. **Fitness Centre:** The ESSC features state-of-the-art fitness equipment, group fitness classes, and personal training sessions.
2. **Swimming Pool:** Members have access to an indoor swimming pool, whirlpool, and sauna.
3. **Golf Course:** The club operates a 18-hole golf course that is open to members and their guests.
4. **Dining and Entertainment:** The ESSC has a restaurant, bar, and lounge that offer a range of food and beverage options.
5. **Social Events:** Throughout the year, the club hosts various social events, including charity functions, tournaments, and networking events.
6. **Programs and Activities:** Members can participate in a variety of programs and activities, such as yoga, Pilates, weightlifting, and team sports (e.g., hockey, basketball).
7. **Catering Services:** The ESSC offers catering services for private events and functions.

**Membership:**
To become a member of the ESSC, individuals must meet certain eligibility criteria, which include:

* Being a resident of Edmonton or surrounding areas
* Being at least 18 years old
* Meeting specific membership requirements (e.g., income level, employment status)

Membership fees vary depending on individual circumstances and are subject to change. It's best to check with the ESSC directly for current pricing and eligibility information.

In summary, the Edmonton Sports and Social Club is a vibrant recreational facility that offers a wide range of services, programs, and amenities for its members.