import Data.List( sortOn )

-- computes the value of a given string 
value :: String -> Int
value line = sum $ map fromEnum line

-- sort input lines by their value
main = interact $ unlines . sortOn value . lines
