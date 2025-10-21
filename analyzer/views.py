from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import AnalyzedString
from .serializers import CreateStringSerializer
from urllib.parse import unquote
import hashlib, re
from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser


class StringView(APIView):

    """
    Unified string view handling:
    - POST /strings/ → create/analyze
    - GET /strings/ → list with filters
    - GET /strings/?query=... → natural language filtering
    - GET /strings/<string_value>/ → fetch single string
    - DELETE /strings/<string_value>/ → delete string
    """
    parser_classes = [JSONParser]

    # ---- POST /strings/ ----
    def post(self, request):
        try:
            # Ensure DRF parses the JSON
            data = request.data
        except ParseError as e:
            # Malformed JSON → 400
            return Response(
                {"detail": f"Invalid JSON: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CreateStringSerializer(data=data)
        serializer = CreateStringSerializer(data=request.data)
        if not serializer.is_valid():

            if any(err.code == "invalid_type" for err_list in serializer.errors.values() for err in err_list):
                # 422 — invalid type
                return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            # 400 — missing or empty
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        obj, created = serializer.save()
        # 409 Conflict — string already exists
        if not created:
            return Response(obj.to_representation(), status=status.HTTP_409_CONFLICT)

        return Response(obj.to_representation(), status=status.HTTP_201_CREATED)

    # ---- GET /strings/ or /strings/<string_value>/ ----
    def get(self, request, string_value: str = None):
        if string_value:
            # Decode URL-encoded string
            raw_value = unquote(string_value)
            sha = hashlib.sha256(raw_value.encode("utf-8")).hexdigest()
            obj = get_object_or_404(AnalyzedString, id=sha)
            return Response(obj.to_representation(), status=status.HTTP_200_OK)

        query = request.query_params.get("query")
        if query:
            return self._natural_language_filter(query)
        return self._list_filtered(request)

    # ---- DELETE /strings/<string_value>/ ----
    def delete(self, request, string_value: None):

        # Handle missing or empty string value safely
        if not string_value or string_value.strip() == "":
            return Response(
                {"detail": "String value is required in the URL."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Decode in case of URL encoding
        raw_value = unquote(string_value)

        # Compute SHA256 of the decoded string
        sha = hashlib.sha256(raw_value.encode("utf-8")).hexdigest()

        # Fetch or return 404 if not found
        obj = get_object_or_404(AnalyzedString, id=sha)

        # Delete the object
        obj.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    # ---- Helper: filtered list ----
    def _list_filtered(self, request):
        qs = AnalyzedString.objects.all()
        is_pal = request.query_params.get("is_palindrome")
        min_length = request.query_params.get("min_length")
        max_length = request.query_params.get("max_length")
        wc = request.query_params.get("word_count")
        cc = request.query_params.get("contains_character")

        if is_pal is not None:
            if is_pal.lower() not in ("true", "false"):
                return Response({"detail": "Invalid is_palindrome value (must be true/false)"},
                                status=status.HTTP_400_BAD_REQUEST)
            qs = qs.filter(is_palindrome=(is_pal.lower() == "true"))

        try:
            if min_length: qs = qs.filter(length__gte=int(min_length))
            if max_length: qs = qs.filter(length__lte=int(max_length))
            if wc: qs = qs.filter(word_count=int(wc))
        except ValueError:
            return Response({"detail": "min_length, max_length, word_count must be integers"},
                            status=status.HTTP_400_BAD_REQUEST)

        if cc:
            if len(cc) != 1:
                return Response({"detail": "contains_character must be a single character"},
                                status=status.HTTP_400_BAD_REQUEST)
            qs = qs.filter(value__icontains=cc)

        data = [obj.to_representation() for obj in qs]
        return Response({"data": data, "count": len(data), "filters_applied": dict(request.query_params)},
                        status=status.HTTP_200_OK)

    # ---- Helper: natural language filter ----
    def _natural_language_filter(self, query):
        try:
            parsed = self.parse_nl_query(query)
        except ValueError:
            return Response({"detail": "Unable to parse natural language query"},
                            status=status.HTTP_400_BAD_REQUEST)

        qs = AnalyzedString.objects.all()
        if "word_count" in parsed: qs = qs.filter(word_count=parsed["word_count"])
        if "is_palindrome" in parsed: qs = qs.filter(is_palindrome=parsed["is_palindrome"])
        if "min_length" in parsed: qs = qs.filter(length__gte=parsed["min_length"])
        if "max_length" in parsed: qs = qs.filter(length__lte=parsed["max_length"])
        if "contains_character" in parsed: qs = qs.filter(value__icontains=parsed["contains_character"])

        data = [obj.to_representation() for obj in qs]
        return Response({
            "data": data,
            "count": len(data),
            "interpreted_query": {"original": query, "parsed_filters": parsed}
        }, status=status.HTTP_200_OK)

    # ---- Static method: parse natural language queries ----
    @staticmethod
    def parse_nl_query(q: str):
        q = q.lower().strip()
        filters = {}

        # Heuristics
        if "single word" in q or re.search(r"\bone word\b|\bword_count\b", q):
            filters["word_count"] = 1
        if "palindrom" in q:
            filters["is_palindrome"] = True
        if "longer than" in q:
            m = re.search(r"longer than (\d+)", q)
            if m:
                filters["min_length"] = int(m.group(1)) + 1
        if "shorter than" in q:
            m = re.search(r"shorter than (\d+)", q)
            if m:
                filters["max_length"] = int(m.group(1)) - 1
        if "contain" in q:
            m = re.search(r"letter ([a-z])", q)
            if m:
                filters["contains_character"] = m.group(1)
        if "first vowel" in q:
            filters["contains_character"] = "a"

        if not filters:
            raise ValueError("Unable to parse natural language query")

        return filters
