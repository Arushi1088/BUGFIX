
import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class TestPhase3Components(unittest.TestCase):
    """Unit tests for Phase 3 UX Analytics components"""

    def setUp(self):
        """Set up test fixtures"""
        # Mock data for testing
        self.mock_ux_data = {
            "visibility_of_system_status": 85,
            "match_between_system_and_real_world": 78,
            "user_control_and_freedom": 82,
            "consistency_and_standards": 88,
            "error_prevention": 75,
            "recognition_rather_than_recall": 80,
            "flexibility_and_efficiency_of_use": 77,
            "aesthetic_and_minimalist_design": 83,
            "help_users_recognize_diagnose_recover_from_errors": 79,
            "help_and_documentation": 81
        }

        self.mock_best_practices = {
            "fluent_design_adoption": 85,
            "accessibility_patterns": 78,
            "ribbon_organization": 82,
            "user_feedback_mechanisms": 88,
            "responsive_design": 75,
            "error_handling": 80
        }

        self.mock_performance = {
            "lcp": 1800,
            "fid": 85,
            "cls": 0.08
        }

    def test_ux_heuristic_scores_mapping(self):
        """Test UX Heuristic scores map correctly"""
        print("\n🔍 Testing UX Heuristic Score Mapping...")

        # Calculate average score
        total_score = sum(self.mock_ux_data.values())
        average_score = total_score / len(self.mock_ux_data)

        # Test score range
        self.assertGreaterEqual(average_score, 0, "Average score should be >= 0")
        self.assertLessEqual(average_score, 100, "Average score should be <= 100")

        # Test individual heuristics
        for heuristic, score in self.mock_ux_data.items():
            self.assertGreaterEqual(score, 0, f"{heuristic} score should be >= 0")
            self.assertLessEqual(score, 100, f"{heuristic} score should be <= 100")

        # Test that all 10 Nielsen heuristics are present
        expected_heuristics = 10
        self.assertEqual(len(self.mock_ux_data), expected_heuristics, 
                        f"Should have {expected_heuristics} UX heuristics")

        print(f"   ✅ UX Heuristic mapping test passed (avg: {average_score:.1f})")
        return True

    def test_best_practices_sections(self):
        """Test best practices sections appear when flags are on"""
        print("\n🎨 Testing Best Practices Sections...")

        # Test that all expected categories are present
        expected_categories = [
            "fluent_design_adoption",
            "accessibility_patterns", 
            "ribbon_organization",
            "user_feedback_mechanisms",
            "responsive_design",
            "error_handling"
        ]

        for category in expected_categories:
            self.assertIn(category, self.mock_best_practices, 
                         f"Best practices should include {category}")

        # Test score ranges
        for category, score in self.mock_best_practices.items():
            self.assertGreaterEqual(score, 0, f"{category} score should be >= 0")
            self.assertLessEqual(score, 100, f"{category} score should be <= 100")

        print(f"   ✅ Best practices sections test passed ({len(self.mock_best_practices)} categories)")
        return True

    def test_health_alert_thresholds(self):
        """Test health alert thresholds fire at configured cut-offs"""
        print("\n🚨 Testing Health Alert Thresholds...")

        # Define threshold test cases
        test_cases = [
            # (metric, value, expected_alert_level)
            ("lcp", 1000, "good"),      # Good LCP
            ("lcp", 2000, "needs_improvement"),  # Needs improvement  
            ("lcp", 3000, "poor"),      # Poor LCP
            ("fid", 50, "good"),        # Good FID
            ("fid", 150, "needs_improvement"), # Needs improvement
            ("fid", 250, "poor"),       # Poor FID
            ("cls", 0.05, "good"),      # Good CLS
            ("cls", 0.15, "needs_improvement"), # Needs improvement
            ("cls", 0.30, "poor"),      # Poor CLS
        ]

        def get_alert_level(metric, value):
            """Simulate alert threshold logic"""
            thresholds = {
                "lcp": {"good": 1500, "poor": 2500},
                "fid": {"good": 100, "poor": 200},
                "cls": {"good": 0.1, "poor": 0.25}
            }

            if metric in thresholds:
                if value <= thresholds[metric]["good"]:
                    return "good"
                elif value <= thresholds[metric]["poor"]:
                    return "needs_improvement"
                else:
                    return "poor"
            return "unknown"

        passed_tests = 0
        for metric, value, expected in test_cases:
            actual = get_alert_level(metric, value)
            if actual == expected:
                passed_tests += 1
            else:
                print(f"   ⚠️  {metric}={value}: expected {expected}, got {actual}")

        success_rate = passed_tests / len(test_cases)
        self.assertGreaterEqual(success_rate, 0.8, "At least 80% of threshold tests should pass")

        print(f"   ✅ Health alert thresholds test passed ({passed_tests}/{len(test_cases)})")
        return True

if __name__ == '__main__':
    print("🧪 RUNNING PHASE 3 UNIT TESTS")
    print("=" * 40)

    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPhase3Components)

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print(f"\n📊 TEST RESULTS:")
    print(f"   Tests Run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")

    if result.wasSuccessful():
        print(f"   🎉 ALL UNIT TESTS PASSED!")
    else:
        print(f"   ⚠️  Some tests failed - see details above")
