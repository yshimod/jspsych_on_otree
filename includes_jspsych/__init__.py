from otree.api import *
import json

doc = """Includes the jsPsych application."""


class C(BaseConstants):
    NAME_IN_URL = 'includes_jspsych'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    jspsychdata = models.LongStringField()

    crt_bat = models.IntegerField(
        label='''
        A bat and a ball cost 22 dollars in total.
        The bat costs 20 dollars more than the ball.
        How many dollars does the ball cost?
        '''
    )
    crt_widget = models.IntegerField(
        label='''
        If it takes 5 machines 5 minutes to make 5 widgets,
        how many minutes would it take 100 machines to make 100 widgets?
        '''
    )
    crt_lake = models.IntegerField(
        label='''
        In a lake, there is a patch of lily pads.
        Every day, the patch doubles in size.
        If it takes 48 days for the patch to cover the entire lake,
        how many days would it take for the patch to cover half of the lake?
        '''
    )


# PAGES
class JsPsych(Page):
    form_model = 'player'
    form_fields = ['jspsychdata']


class CognitiveReflectionTest(Page):
    form_model = 'player'
    form_fields = ['crt_bat', 'crt_widget', 'crt_lake']


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            indented_data = json.dumps(
                json.loads(player.jspsychdata),
                indent = 4
            )
        )


def custom_export(players):
    yield [
        'session',
        'participant_code',
        'Vegetables',
        'Meat',
        'Fruit',
        'average_score',
        'average_response_time'
    ]

    for p in players:
        participant = p.participant
        session = p.session

        surveyresponse = [-1]*3
        average_score = -1
        average_response_time = -1

        jspsychdata = p.field_maybe_none("jspsychdata")
        if jspsychdata:
            parsed_data = json.loads(jspsychdata)["trials"]

            taskdata = []
            for v in parsed_data:
                if v["internal_node_id"] == "0.0-2.0":
                    surveyresponse = [
                        v["response"]["Vegetables"],
                        v["response"]["Meat"],
                        v["response"]["Fruit"]
                    ]

                elif v["internal_node_id"][:9] == "0.0-4.0-1":
                    taskdata.append(
                        [(v["correct"]), float(v["rt"])]
                    )

            average_score = sum([v[0] for v in taskdata]) / len(taskdata)
            average_response_time = sum([v[1] for v in taskdata]) / len(taskdata)


        yield [
            session.code,
            participant.code,
            surveyresponse[0],
            surveyresponse[1],
            surveyresponse[2],
            average_score,
            average_response_time
        ]



page_sequence = [JsPsych, CognitiveReflectionTest, Results]
