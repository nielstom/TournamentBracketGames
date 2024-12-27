import plotly.graph_objects as go
import random


def play_match(player1, player2):
    return random.choice([player1, player2])


def create_bracket(num_players=8):
    players = [f"P{i + 1}" for i in range(num_players)]
    random.shuffle(players)

    rounds = []
    current_round = players
    while len(current_round) > 1:
        rounds.append(current_round)
        winners = []
        for i in range(0, len(current_round), 2):
            winner = play_match(current_round[i], current_round[i + 1])
            winners.append(winner)
        current_round = winners
    rounds.append(current_round)  # Final winner

    fig = go.Figure()

    y_positions = []
    for round_num, round_players in enumerate(rounds):
        if round_num == 0:
            y_pos = [i for i in range(len(round_players))]
        else:
            y_pos = []
            for i in range(0, len(round_players)):
                y_pos.append((y_positions[round_num - 1][i * 2] + y_positions[round_num - 1][i * 2 + 1]) / 2)
        y_positions.append(y_pos)

    for round_num, round_players in enumerate(rounds):
        for i, player in enumerate(round_players):
            fig.add_shape(
                type="rect",
                x0=round_num - 0.2, y0=y_positions[round_num][i] - 0.2,
                x1=round_num + 0.2, y1=y_positions[round_num][i] + 0.2,
                line=dict(color="Black", width=2),
                fillcolor="White"
            )
            fig.add_annotation(
                x=round_num, y=y_positions[round_num][i],
                text=player,
                showarrow=False
            )

        if round_num < len(rounds) - 1:
            for i in range(0, len(round_players), 2):
                next_pos = y_positions[round_num + 1][i // 2]
                fig.add_trace(go.Scatter(
                    x=[round_num + 0.2, round_num + 0.6, round_num + 0.6, round_num + 1 - 0.2],
                    y=[y_positions[round_num][i], y_positions[round_num][i], next_pos, next_pos],
                    mode='lines',
                    line=dict(color='black', width=2),
                    hoverinfo='none'
                ))
                if i + 1 < len(round_players):
                    fig.add_trace(go.Scatter(
                        x=[round_num + 0.2, round_num + 0.6, round_num + 0.6, round_num + 1 - 0.2],
                        y=[y_positions[round_num][i + 1], y_positions[round_num][i + 1], next_pos, next_pos],
                        mode='lines',
                        line=dict(color='black', width=2),
                        hoverinfo='none'
                    ))

    fig.update_layout(
        title='8-Player Tournament Bracket',
        xaxis=dict(
            title='Rounds',
            tickmode='array',
            tickvals=list(range(len(rounds))),
            ticktext=[f'Round {i + 1}' for i in range(len(rounds))],
            range=[-0.5, len(rounds) - 0.5]
        ),
        yaxis=dict(showticklabels=False, range=[-1, num_players]),
        showlegend=False,
        height=600,
        width=800,
        plot_bgcolor='white'
    )

    fig.show()


create_bracket()
