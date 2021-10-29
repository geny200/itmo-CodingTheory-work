import Chanel.BEC.TestProbabilities (probabilitiesTest)
import Decoder.TestPolar (polarTest)

main :: IO ()
main =
  do
    probabilitiesTest
    polarTest
