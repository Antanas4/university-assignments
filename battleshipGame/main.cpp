#include <iostream>
#include <vector>
#include <map>
#include <set>
#include <algorithm>
#include <unistd.h>
using namespace std;

class playerBase
{
    protected:
        char **playersBoard;
        char **opponentsBoard; 
        map< string, vector<string> > ship;
        set<string> pastMoves;
        set<string> uniqueInputCoordinates;
        bool winner;
    public:
        playerBase():winner(0), playersBoard(0), opponentsBoard(0) {}
        playerBase(const string carriernm,const string battleshipnm, const string cruisernm, const string submarinenm, const string destroyernm) 
        {
            playersBoard = new char*[10];
            opponentsBoard = new char*[10];
            for(int i=0; i<10; i++)
            {
                playersBoard[i] = new char[10];
                opponentsBoard[i] = new char[10];
            }

            for (int i = 0; i < 10; i++) 
            {
                for (int j = 0; j < 10; j++) 
                {
                    playersBoard[i][j] = 'x';
                    opponentsBoard[i][j] = 'x';
                }
            }
            ship[carriernm];
            ship[battleshipnm];
            ship[cruisernm];
            ship[submarinenm];
            ship[destroyernm];
        } 
        ~playerBase(){} 
        
};

class players : private playerBase
{
    public:
    players (const string carriernm,const string battleshipnm, const string cruisernm,const string submarinenm, const string destroyernm): 
    playerBase(carriernm, battleshipnm, cruisernm, submarinenm, destroyernm){}

    ~players(){}   

        void askForShipInputCoordinates(string shipType, int shipLength, map<string, int> boardCoordinates)
        {   
            bool validCoordinates = false;
            bool validPlacement = false;
            string startCoordinate, endCoordinate;
            int start, end, startRow, endRow, startCol, endCol;
            while(!validCoordinates || !validPlacement)
            {
                cout << "Enter the start and end coordinate for " << shipType << " (length " << shipLength << "): ";
                cin >> startCoordinate >> endCoordinate;
                
                if (boardCoordinates.find(startCoordinate) == boardCoordinates.end() || boardCoordinates.find(endCoordinate) == boardCoordinates.end()) 
                {
                    validCoordinates = false;
                    cout << "Coordinates out of range!" << endl;
                }
                else
                {
                    validCoordinates = true;
                    validPlacement = true;
                }

                
                start = boardCoordinates[startCoordinate];
                end = boardCoordinates[endCoordinate];

                startRow = start / 10;
                startCol = start % 10;

                endRow = end / 10;
                endCol = end % 10;

                if (startRow != endRow && startCol != endCol && validCoordinates == true)
                {
                    validCoordinates = false;
                    cout << "The ship must be placed horizontally or vertically!" << endl;
                }
                
                string tempCoordinate;

                if (startRow == endRow && validCoordinates == true)
                {
                    for (int col = startCol; col <= endCol; col++)
                    {
                        tempCoordinate = to_string(startRow) + string(1, col + 'a');
                        if (uniqueInputCoordinates.count(tempCoordinate) > 0)
                        {
                            cout << "The ship coordinates are repeating! Please enter valid coordinates." << endl;
                            validCoordinates = false;
                            break;
                        }
                        
                    }
                }
                else if (startCol == endCol && validCoordinates == true)
                {
                    for (int row = startRow; row <= endRow; row++)
                    {
                        tempCoordinate = to_string(row) + string(1, startCol + 'a');
                        if (uniqueInputCoordinates.count(tempCoordinate) > 0)
                        {
                            cout << "The ship coordinates are repeating! Please enter valid coordinates." << endl;
                            validCoordinates = false;
                            break;
                        }
                    }
                }
                if (startRow == endRow && abs(startCol - endCol) + 1 != shipLength && validCoordinates == true)
                {
                    cout << "Ship length does not match" << endl;
                    validPlacement = false;
                }
                else if (startCol == endCol && abs(startRow - endRow) + 1 != shipLength && validCoordinates == true)
                {
                    cout << "Ship length does not match" << endl;
                    validPlacement = false;
                }

                if (startRow == endRow && validCoordinates == true && validPlacement == true)
                {
                    for (int col = startCol; col <= endCol; col++)
                    {
                        tempCoordinate = to_string(startRow) + string(1, col + 'a'); 
                        ship[shipType].push_back(tempCoordinate);
                        uniqueInputCoordinates.insert(tempCoordinate);
                    }
                }
                else if (startCol == endCol && validCoordinates == true && validPlacement == true)
                {
                    for (int row = startRow; row <= endRow; row++)
                    {
                        tempCoordinate = to_string(startCol) + string(1, row + 'a'); 
                        ship[shipType].push_back(tempCoordinate);
                        uniqueInputCoordinates.insert(tempCoordinate);
                    }
                }

            }

        }
        void deployShips(map <string, int> boardCoordinates)
        {   
            for (map<string, vector<string> >::iterator shipType = ship.begin(); shipType != ship.end(); ++shipType)
            {
                vector<string>& shipCoordinates = shipType->second;

                string startCoordinate = shipCoordinates.front();
                string endCoordinate = shipCoordinates.back();

                int start = boardCoordinates[startCoordinate];
                int end = boardCoordinates[endCoordinate];

                int startRow = start / 10;
                int startCol = start % 10;

                int endRow = end / 10;
                int endCol = end % 10;

                if (startRow == endRow)
                {
                    for (int col=startCol; col<=endCol; col++)
                    {
                        if (col == startCol)
                        {playersBoard[startRow][col] ='[';}
                        else if (col == endCol)
                        {playersBoard[startRow][col] = ']';}
                        else
                        {playersBoard[startRow][col] = ' ';}
                    }
                }
                else if (startCol == endCol)
                {
                    for (int row=startRow; row<=endRow; row++)
                    {
                        if (row == startRow)
                        {playersBoard[row][startCol] = '[';}
                        if (row == endRow)
                        {playersBoard[row][startCol] = ']';}
                        else
                        {playersBoard[row][startCol] = ' ';}
                    }
                }
            }
        }
        bool validHitMove(string value)
        {
            set<string>::iterator it = find(pastMoves.begin(), pastMoves.end(), value);
            if (it != pastMoves.end())
            {return false;}
            else
            {
                pastMoves.insert(value);
                return true;
            }
        }
        
        players hitBoard (string currentMove)
        {
            for (map<string, vector<string> >::iterator it = ship.begin(); it != ship.end(); ++it) 
            {
                vector<string>& vec = it->second;  
                vector<string>::iterator pos = find(vec.begin(), vec.end(), currentMove);
                if (find(vec.begin(), vec.end(), currentMove) != vec.end()) 
                {
                    vec.erase(pos);
                    break;
                }
            }
            return *this;
        }
        pair<players, players> updateBoard (players& x, string currentMove, map <string, int> boardCoordinates)
        {
            int row = boardCoordinates[currentMove] / 10;
            int col = boardCoordinates[currentMove] % 10;

            if (x.playersBoard[row][col] == '[' || x.playersBoard[row][col] == ']' || x.playersBoard[row][col] == ' ')
            {
                x.playersBoard[row][col] = 'h';
                opponentsBoard[row][col] = 'h';
                cout << "You just hit your opponent's ship!" << endl;
            } 
            else
            {
                x.playersBoard[row][col] = 'm';
                opponentsBoard[row][col] = 'm';
                cout << "You Missed!" << endl;
            }

            pair<players, players> updatePlayers(*this, x);
            return updatePlayers;
        }

        void operator ++()
        {
            cout << "   ";
            for (int i='A'; i!='K'; i++)
            {
                cout << string(1, i) << " ";
            }
            cout << endl;
            for (int i=0; i<10; i++)
            {
                cout << i << "  ";
                for (int j=0; j<10; j++)
                {
                    cout << opponentsBoard[i][j];
                    if (j != 9) 
                    cout << "|";
                }
                cout << endl;
            }
            cout << "------------------------" << endl;
            cout << "   ";
            for (int i='A'; i!='K'; i++)
            {
                cout << string(1, i) << " ";
            }
            cout << endl;
            for (int i=0; i<10; i++)
            {
                cout << i << "  ";
                for (int j=0; j<10; j++)
                {
                    cout << playersBoard[i][j];
                    if (j != 9) 
                    cout << "|";
                }
                cout << endl;
            }
            sleep(6);
            system("clear");
        }
        pair<players, players> checkForWinner (players& x, bool& play)
        {
            if (ship["carrier"].size() == 0 && ship["battleship"].size() == 0 && ship["cruiser"].size() == 0 && ship["submarine"].size() == 0 && ship["destroyer"].size() == 0)
            {
                winner = true;
                play = false;
            }
            else if (x.ship["carrier"].size() == 0 && x.ship["battleship"].size() == 0 && x.ship["cruiser"].size() == 0 && x.ship["submarine"].size() == 0 && x.ship["destroyer"].size() == 0)
            {
                winner = true;
                play = false;
            }
            else
            {
                play = true;
            }
            pair<players, players> updatePlayers(*this, x);
            return updatePlayers;
        }
        bool getWinner()
        {
            return winner;
        }
};
map <string, int> boardCoordinates;
void createBoardCoordinates(map<string, int>& board);
string askForMoveCoordinates(players player[], int currentPlayer);
int main ()
{
    bool play = true;

    string currentMove = "";
    players player[2] = {players("carrier", "battleship", "cruiser", "submarine", "destroyer"), 
        players( "carrier", "battleship", "cruiser", "submarine", "destroyer")};
        
    createBoardCoordinates(boardCoordinates);

    for (int i=0; i<2; i++)
    {
        cout << "Deploy ships for " << "player " << i+1 << "." << endl;
        player[i].askForShipInputCoordinates("carrier", 5, boardCoordinates);
        player[i].askForShipInputCoordinates("battleship", 4, boardCoordinates);
        player[i].askForShipInputCoordinates("cruiser", 3, boardCoordinates);
        player[i].askForShipInputCoordinates("submarine", 3, boardCoordinates);
        player[i].askForShipInputCoordinates("destroyer", 2, boardCoordinates);
        player[i].deployShips(boardCoordinates);
        system("clear");
    }

    while (play)
    {
        currentMove = askForMoveCoordinates(player, 0);
        player[1].hitBoard(currentMove);
        player[0].updateBoard(player[1], currentMove, boardCoordinates);
        ++player[0];
        player[0].checkForWinner(player[1], play);
        if (play)
        {
            currentMove = askForMoveCoordinates(player, 1);
            player[0].hitBoard(currentMove);
            player[1].updateBoard(player[0], currentMove, boardCoordinates);
            ++player[1];
            player[1].checkForWinner(player[0], play);
        }
    }

    if (player[0].getWinner() == true)
    {
        cout << "PLayer 1 wins!" << endl;
        ++player[0];
    }
    else
    {
        cout << "Player 2 wins!" << endl;
        ++player[1];
    }
    cout << "GAME END";


    return 0;
}
void createBoardCoordinates(map<string, int>& board)
{   
    string textCoordinate = "";
    
    for (int row=0; row<10; row++)
    {
        for (int col='a'; col<='j'; col++)
        {
            textCoordinate = to_string(row) + string(1, col);
            board[textCoordinate] = row * 10 + (col - 'a');
        }
    }
}


string askForMoveCoordinates(players player[], int currentPlayer)
{
    bool askForMove = true;
    string value;
    while (askForMove)
    {
        try
        {
            cout << "Enter the coordinate you want to hit: ";
            cin >> value;
            map<string, int>::iterator it = boardCoordinates.find(value);
            if (it != boardCoordinates.end() && player[currentPlayer].validHitMove(value) == true)
            {   
                askForMove = false;
                break;
            }
            else
            {
                throw(value);
            }   
        }
        catch(string val)
        {
            cout << "The coordinates does not exist or you have already made this move! " << value << endl;
            askForMove = true;
            sleep(2);
            system("clear");
        }
    }
    return value;
}
