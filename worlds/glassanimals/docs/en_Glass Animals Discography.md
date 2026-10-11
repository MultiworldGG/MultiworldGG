# Glass Animals Discography

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## What does randomization do in this implementation?

Glass Animals' albums are divided into regions, and listening to each band's songs acts as checks. Each song is an item
you can find in the multiworld; once you've collected a song's item you can listen to it to earn its location check.
Which albums are enabled (Dreamland, I Love You So F***ing Much, How to Be a Human Being, and Zaba) is controlled by
options in the YAML file, along with whether the short Home Movie tracks from Dreamland are included.

## What is the goal of Glass Animals Discography?

The goal is to collect every included song item and listen to every song in all enabled albums. The client used for this
implementation keeps track of your progress internally, and the goal is reached once every enabled album has been fully
collected and listened to.