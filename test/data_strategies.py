from hypothesis import given, strategies as st
from hypothesis.extra import pandas as st_pd
from faker import Faker
import datetime
import pandas as pd
import numpy as np

fake = Faker("ja_JP")


def real_name_fake():
    return fake.name()


def team_name_fake():
    return fake.company()


@st.composite
def date_string_strategy(draw):
    dt_obj = draw(
        st.datetimes(
            min_value=datetime.datetime(2020, 1, 1),
            max_value=datetime.datetime(2028, 12, 31),
        )
    )
    return dt_obj.strftime("%Y-%m-%d")


@st.composite
def player_name_strategy(draw):
    return draw(st.just(real_name_fake()))


@st.composite
def score_strategy(draw):
    value = draw(st.integers(min_value=-300, max_value=2000))
    return value * 100


@st.composite
def team_strategy(draw):
    player_names = [
        real_name_fake() for _ in range(draw(st.integers(min_value=18, max_value=40)))
    ]
    team_names = [
        team_name_fake() for _ in range(draw(st.integers(min_value=4, max_value=10)))
    ]

    # チーム名を均等に割り当てる
    n_players = len(player_names)
    n_teams = len(team_names)
    # チーム名リストを繰り返して人数分にする
    assigned_teams = (team_names * ((n_players + n_teams - 1) // n_teams))[:n_players]
    # シャッフルしてランダム性を持たせる
    assigned_teams = draw(st.permutations(assigned_teams))

    df = pd.DataFrame(
        {
            "選手名": player_names,
            "チーム名": assigned_teams,
        }
    )
    return df


# --- DataFrame生成のメインストラテジー ---
def match_result_dataframe_strategy(min_rows: int = 1, max_rows: int = 10):
    return st_pd.data_frames(
        columns=[
            st_pd.column("date", elements=date_string_strategy(), dtype=str),
            st_pd.column(
                "times", elements=st.integers(min_value=1, max_value=5), dtype=int
            ),
            st_pd.column("player1", elements=player_name_strategy(), dtype=str),
            st_pd.column("player2", elements=player_name_strategy(), dtype=str),
            st_pd.column("player3", elements=player_name_strategy(), dtype=str),
            st_pd.column("player4", elements=player_name_strategy(), dtype=str),
            st_pd.column("score1", elements=score_strategy(), dtype=int),
            st_pd.column("score2", elements=score_strategy(), dtype=int),
            st_pd.column("score3", elements=score_strategy(), dtype=int),
            st_pd.column("score4", elements=score_strategy(), dtype=int),
        ],
        index=st_pd.range_indexes(min_size=min_rows, max_size=max_rows),
    ).map(lambda df: df.assign(date=pd.to_datetime(df["date"])))


def match_result_dataframe_strategy_from_team(
    team_df, min_rows: int = 1, max_rows: int = 10
):
    team_to_players = team_df.groupby("チーム名")["選手名"].apply(list).to_dict()
    team_names = list(team_to_players.keys())

    def row_strategy():
        # 4つの異なるチームをランダムに選ぶ
        selected_teams = st.sampled_from(team_names).flatmap(
            lambda t1: st.sampled_from([t for t in team_names if t != t1]).flatmap(
                lambda t2: st.sampled_from(
                    [t for t in team_names if t not in [t1, t2]]
                ).flatmap(
                    lambda t3: st.sampled_from(
                        [t for t in team_names if t not in [t1, t2, t3]]
                    ).map(lambda t4: [t1, t2, t3, t4])
                )
            )
        )
        # 各チームから1人ずつ選ぶ＋スコアも生成
        return selected_teams.flatmap(
            lambda teams: st.tuples(
                st.sampled_from(team_to_players[teams[0]]),
                st.sampled_from(team_to_players[teams[1]]),
                st.sampled_from(team_to_players[teams[2]]),
                st.sampled_from(team_to_players[teams[3]]),
                score_strategy(),
                score_strategy(),
                score_strategy(),
                score_strategy(),
                date_string_strategy(),
                st.integers(min_value=1, max_value=5),
            ).map(
                lambda vals: {
                    "player1": vals[0],
                    "player2": vals[1],
                    "player3": vals[2],
                    "player4": vals[3],
                    "score1": vals[4],
                    "score2": vals[5],
                    "score3": vals[6],
                    "score4": vals[7],
                    "date": vals[8],
                    "times": vals[9],
                }
            )
        )

    return st.lists(row_strategy(), min_size=min_rows, max_size=max_rows).map(
        lambda rows: pd.DataFrame(rows)
    )


team = team_strategy()
team_df = team.example()
print(team_df)
result_df = match_result_dataframe_strategy_from_team(
    team_df, min_rows=5, max_rows=10
).example()
print(result_df)
