import json
import re

from django.core.management.base import BaseCommand

from faculty_planner.models import NTAChallenge, NTAFact, NTABadge, \
                        NTAChallengeFacts, NTAChallengeBadge, NTACategory, \
                        NTAChallengeCategory


class Command(BaseCommand):
    help = "Imports name that animal data"

    def __init__(self):
        super(Command, self).__init__()
        self.verbosity = 1
        self.data_file = None

    def add_arguments(self, parser):
        parser.add_argument('data_file', type=str)

    def handle(self, **options):
        self.verbosity = int(options.get('verbosity', 1))
        self.data_file = options.get('data_file')
        data = {}

        self.verbose_print('Loading file "{}" ...'.format(self.data_file))
        try:
            data = json.load(open(self.data_file, encoding='utf-8'))
        except json.decoder.JSONDecodeError:
            self.verbose_print('Could not parse json.')
        self.verbose_print('Deleting existing objects...')
        # NOTE: THIS DELETES ALL CHALLENGES AND BADGES
        NTAChallengeCategory.objects.all().delete()
        NTACategory.objects.all().delete()
        NTAChallengeFacts.objects.all().delete()
        NTAChallengeBadge.objects.all().delete()
        NTAChallenge.objects.all().delete()
        NTAFact.objects.all().delete()
        NTABadge.objects.all().delete()
        self.verbose_print('Completed.')
        self.verbose_print('Loading animals...')
        # create animals for challenge
        for animal in data['Animals']:
            if animal['Selected']=='x':
                name = animal['Name'].title()
                difficulty = animal['Difficulty'].title()
                genus = animal['Genus'].title()
                category, created = NTACategory.objects.get_or_create(name=genus)
                challenge = NTAChallenge.objects.create(animal_name_utterance=name, difficulty=difficulty)
                NTAChallengeCategory.objects.create(challenge=challenge,category=category)

                NTAChallengeFacts.objects \
                    .create(challenge=challenge, fact=NTAFact.objects.create(utterance=animal['Clue 1']), order=1)
                NTAChallengeFacts.objects \
                    .create(challenge=challenge, fact=NTAFact.objects.create(utterance=animal['Clue 2']), order=2)
                NTAChallengeFacts.objects \
                    .create(challenge=challenge, fact=NTAFact.objects.create(utterance=animal['Clue 3']), order=3)
                NTAChallengeFacts.objects \
                    .create(challenge=challenge, fact=NTAFact.objects.create(utterance=animal['Clue 4']), order=4)
                NTAChallengeFacts.objects \
                    .create(challenge=challenge, fact=NTAFact.objects.create(utterance=animal['Clue 5']), order=5)

        # create a badge
        for badge_data in data['Badges']:
            regex = re.compile('Animal name *')

            keys = set([])
            for key, value in badge_data.items():
                keys.add(key)

            animals_key = list(filter(regex.match, keys))

            title = badge_data["Badge name"]
            description = badge_data.get("Description", title)
            badge = NTABadge.objects.create(title=title, description=description)

            for animal_key in animals_key:
                name = badge_data[animal_key].title()
                challenge = NTAChallenge.objects.filter(animal_name_utterance=name)

                if challenge:
                    NTAChallengeBadge.objects.create(badge=badge, challenge=challenge.first())

        self.verbose_print("Done.")

    def verbose_print(self, msg, error=False):
        if error:
            self.stderr.write(msg)
        elif self.verbosity >= 1:
            self.stdout.write(msg)
